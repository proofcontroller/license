"""License server HTTP API.

Base path /v1. Called only by installed controllers (outbound HTTPS 443
from the customer's host). Never receives arena data, proof bundles, or
cloud credentials: only a key, an install id, a host fingerprint, and the
controller version.
"""

from __future__ import annotations

import hashlib
import threading
import time
from collections import defaultdict, deque
from datetime import timedelta
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from . import __version__, keys, registry, settings, token

app = FastAPI(title="Proof Controller License Server", version=__version__)

V1 = "/v1"


@lru_cache(maxsize=1)
def _signing_key():
    return keys.load_signing_key()


def reset_cache() -> None:
    """Drop the cached signing key (tests, key rotation)."""
    _signing_key.cache_clear()


def kid() -> str:
    return hashlib.sha256(keys.public_pem(_signing_key()).encode()).hexdigest()[:16]


# ---- tiny per-client rate limit: 30 requests / 60 s on key-bearing routes ----
_hits: dict[str, deque] = defaultdict(deque)
_lock = threading.Lock()
RATE_MAX, RATE_WINDOW = 30, 60.0


def _rate_limit(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    t = time.monotonic()
    with _lock:
        q = _hits[ip]
        while q and t - q[0] > RATE_WINDOW:
            q.popleft()
        if len(q) >= RATE_MAX:
            raise HTTPException(status_code=429, detail="too many requests")
        q.append(t)


# ---- models ----
class KeyIn(BaseModel):
    key: str = Field(min_length=8, max_length=64)


class ActivateIn(KeyIn):
    install_id: str = Field(min_length=8, max_length=64)
    fingerprint: str = Field(min_length=16, max_length=128)
    version: str | None = Field(default=None, max_length=32)


class InstallIn(BaseModel):
    install_id: str = Field(min_length=8, max_length=64)
    fingerprint: str = Field(min_length=16, max_length=128)
    version: str | None = Field(default=None, max_length=32)


# ---- helpers ----
def _check_key(rec: dict | None) -> dict:
    problem = registry.key_problem(rec)
    if problem == "unknown license key":
        raise HTTPException(status_code=404, detail="Invalid license key")
    if problem:
        raise HTTPException(status_code=403, detail=problem.capitalize())
    return rec


def _summary(rec: dict) -> dict:
    return {
        "status": "valid",
        "tier": rec["tier"],
        "licensed_to": rec["licensed_to"],
        "seats": rec["seats"],
        "expires_at": rec["expires_at"],
        "key_masked": "PCL-****-****-****-" + rec["last_four"],
        "installs_used": registry.active_installs(rec["id"]),
        "installs_max": rec["max_installs"],
    }


def issue_token(rec: dict, install_id: str, fingerprint: str, *, offline: bool = False,
                days: int | None = None) -> str:
    """Sign a license token for one install.

    free and gov: no online refresh required (refresh_by is null).
    pro and max: refresh_by = now + REFRESH_DAYS.
    offline=True (Gov license file): no refresh; expiry is the key's expiry
    or `days` from now, whichever is sooner.
    """
    now = registry.now()
    exp = registry.parse(rec["expires_at"])
    if days:
        cap = now + timedelta(days=days)
        exp = min(exp, cap) if exp else cap
    needs_refresh = rec["tier"] in ("pro", "max") and not offline
    claims = {
        "iss": "proofcontroller",
        "kid": kid(),
        "lic": rec["id"],
        "install_id": install_id,
        "fingerprint": fingerprint,
        "tier": rec["tier"],
        "seats": rec["seats"],
        "licensed_to": rec["licensed_to"],
        "issued_at": registry.iso(now),
        "expires_at": registry.iso(exp),
        "refresh_by": registry.iso(now + timedelta(days=settings.REFRESH_DAYS)) if needs_refresh else None,
        "offline": offline,
    }
    return token.sign(claims, _signing_key())


def _install_for(body: InstallIn) -> dict:
    inst = registry.get_install(body.install_id)
    if inst is None:
        raise HTTPException(status_code=404, detail="Unknown install")
    if inst["fingerprint"] != body.fingerprint:
        raise HTTPException(status_code=403, detail="Host fingerprint does not match this install")
    return inst


# ---- routes ----
@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok", "service": "proof-license", "version": __version__}


@app.get(f"{V1}/public-key")
def public_key() -> dict:
    return {"alg": "Ed25519", "kid": kid(), "pem": keys.public_pem(_signing_key())}


@app.post(f"{V1}/validate")
def validate(body: KeyIn, request: Request) -> dict:
    _rate_limit(request)
    return _summary(_check_key(registry.find_key(body.key)))


@app.post(f"{V1}/activate")
def activate(body: ActivateIn, request: Request) -> dict:
    _rate_limit(request)
    rec = _check_key(registry.find_key(body.key))
    existing = registry.get_install(body.install_id)
    rebinding_same = (existing and existing["key_id"] == rec["id"] and existing["status"] == "active")
    if not rebinding_same and registry.active_installs(rec["id"]) >= rec["max_installs"]:
        raise HTTPException(
            status_code=409,
            detail=f"Install limit reached ({rec['max_installs']}). Deactivate another install first.")
    registry.bind(rec["id"], body.install_id, body.fingerprint, body.version)
    return {"token": issue_token(rec, body.install_id, body.fingerprint), **_summary(rec), "status": "active"}


@app.post(f"{V1}/refresh")
def refresh(body: InstallIn) -> dict:
    inst = _install_for(body)
    if inst["status"] != "active":
        raise HTTPException(status_code=403, detail="Install is not active")
    rec = _check_key(registry.get_key(inst["key_id"]))
    registry.touch(body.install_id, body.version)
    return {"token": issue_token(rec, body.install_id, body.fingerprint), "status": "active"}


@app.post(f"{V1}/deactivate")
def deactivate(body: InstallIn) -> dict:
    _install_for(body)
    registry.release(body.install_id)
    return {"status": "deactivated"}
