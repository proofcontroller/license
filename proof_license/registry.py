"""License registry: keys and the installs bound to them (SQLite).

Plaintext license keys are never stored. Only a SHA-256 hash of the key,
plus the last four characters for display.
"""

from __future__ import annotations

import hashlib
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import settings

# Crockford-style base32 alphabet: no I, L, O, U, so keys read and type cleanly.
ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

SCHEMA = """
CREATE TABLE IF NOT EXISTS license_key (
    id            TEXT PRIMARY KEY,
    key_hash      TEXT NOT NULL UNIQUE,
    last_four     TEXT NOT NULL,
    tier          TEXT NOT NULL,
    seats         INTEGER NOT NULL DEFAULT 1,
    max_installs  INTEGER NOT NULL DEFAULT 1,
    licensed_to   TEXT NOT NULL,
    email         TEXT,
    expires_at    TEXT,
    status        TEXT NOT NULL DEFAULT 'active',
    created_at    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS install (
    install_id    TEXT PRIMARY KEY,
    key_id        TEXT NOT NULL REFERENCES license_key(id),
    fingerprint   TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'active',
    version       TEXT,
    activated_at  TEXT NOT NULL,
    last_seen_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS install_key ON install (key_id, status);
"""


def now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime | None) -> str | None:
    return dt.isoformat().replace("+00:00", "Z") if dt else None


def parse(ts: str | None) -> datetime | None:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else None


def normalize_key(key: str) -> str:
    """Uppercase, strip spaces and dashes, map look-alikes (O->0, I/L->1)."""
    k = "".join(ch for ch in key.upper() if ch.isalnum())
    return k.replace("O", "0").replace("I", "1").replace("L", "1")


def hash_key(key: str) -> str:
    return hashlib.sha256(normalize_key(key).encode("ascii")).hexdigest()


def new_key() -> str:
    """PCL-XXXX-XXXX-XXXX-XXXX: 80 random bits after the prefix."""
    body = "".join(secrets.choice(ALPHABET) for _ in range(16))
    return "PCL-" + "-".join(body[i:i + 4] for i in range(0, 16, 4))


@contextmanager
def connect(path: Path | None = None):
    path = path or settings.registry_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def issue(tier: str, licensed_to: str, *, seats: int = 1, max_installs: int = 1,
          email: str | None = None, days: int | None = None) -> tuple[str, dict]:
    """Create a key. Returns (plaintext key, record). The plaintext is shown once."""
    if tier not in settings.TIERS:
        raise ValueError(f"tier must be one of {settings.TIERS}")
    if seats < 1 or max_installs < 1:
        raise ValueError("seats and max_installs must be >= 1")
    key = new_key()
    rec = {
        "id": "lic_" + secrets.token_hex(8),
        "key_hash": hash_key(key),
        "last_four": key[-4:],
        "tier": tier,
        "seats": seats,
        "max_installs": max_installs,
        "licensed_to": licensed_to,
        "email": email,
        "expires_at": iso(now() + timedelta(days=days)) if days else None,
        "status": "active",
        "created_at": iso(now()),
    }
    with connect() as c:
        c.execute(
            "INSERT INTO license_key VALUES (:id,:key_hash,:last_four,:tier,:seats,"
            ":max_installs,:licensed_to,:email,:expires_at,:status,:created_at)", rec)
    return key, rec


def find_key(key: str) -> dict | None:
    with connect() as c:
        row = c.execute("SELECT * FROM license_key WHERE key_hash = ?", (hash_key(key),)).fetchone()
    return dict(row) if row else None


def get_key(key_id: str) -> dict | None:
    with connect() as c:
        row = c.execute("SELECT * FROM license_key WHERE id = ?", (key_id,)).fetchone()
    return dict(row) if row else None


def list_keys() -> list[dict]:
    with connect() as c:
        rows = c.execute(
            "SELECT k.*, (SELECT count(*) FROM install i WHERE i.key_id = k.id AND i.status='active')"
            " AS active_installs FROM license_key k ORDER BY created_at").fetchall()
    return [dict(r) for r in rows]


def set_key_status(key_id: str, status: str) -> bool:
    with connect() as c:
        cur = c.execute("UPDATE license_key SET status = ? WHERE id = ?", (status, key_id))
    return cur.rowcount == 1


def get_install(install_id: str) -> dict | None:
    with connect() as c:
        row = c.execute("SELECT * FROM install WHERE install_id = ?", (install_id,)).fetchone()
    return dict(row) if row else None


def active_installs(key_id: str) -> int:
    with connect() as c:
        return c.execute("SELECT count(*) FROM install WHERE key_id = ? AND status = 'active'",
                         (key_id,)).fetchone()[0]


def bind(key_id: str, install_id: str, fingerprint: str, version: str | None) -> None:
    ts = iso(now())
    with connect() as c:
        c.execute(
            "INSERT INTO install (install_id, key_id, fingerprint, status, version, activated_at, last_seen_at)"
            " VALUES (?,?,?,'active',?,?,?)"
            " ON CONFLICT(install_id) DO UPDATE SET key_id=excluded.key_id, fingerprint=excluded.fingerprint,"
            " status='active', version=excluded.version, last_seen_at=excluded.last_seen_at",
            (install_id, key_id, fingerprint, version, ts, ts))


def touch(install_id: str, version: str | None) -> None:
    with connect() as c:
        c.execute("UPDATE install SET last_seen_at = ?, version = COALESCE(?, version) WHERE install_id = ?",
                  (iso(now()), version, install_id))


def release(install_id: str) -> None:
    with connect() as c:
        c.execute("UPDATE install SET status = 'deactivated', last_seen_at = ? WHERE install_id = ?",
                  (iso(now()), install_id))


def key_problem(rec: dict | None) -> str | None:
    """Why a key cannot be used right now, or None if it can."""
    if rec is None:
        return "unknown license key"
    if rec["status"] != "active":
        return "license key revoked"
    exp = parse(rec["expires_at"])
    if exp and exp <= now():
        return "license key expired"
    return None
