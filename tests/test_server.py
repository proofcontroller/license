"""License server tests: real Ed25519 key, real SQLite registry.

verify_v1() below is the token contract. The controller's verifier
(proofcontroller/proofcontroller, proof_controller/licensing.py) must accept exactly
what this accepts.
"""

import base64
import json

import pytest
from cryptography.hazmat.primitives import serialization
from fastapi.testclient import TestClient

IID, FP = "inst_" + "a" * 32, "f" * 64


def verify_v1(tok: str, pub_pem: str) -> dict:
    prefix, body, sig = tok.split(".")
    assert prefix == "v1"
    pub = serialization.load_pem_public_key(pub_pem.encode())
    pad = lambda s: s + "=" * (-len(s) % 4)  # noqa: E731
    pub.verify(base64.urlsafe_b64decode(pad(sig)), f"{prefix}.{body}".encode())
    return json.loads(base64.urlsafe_b64decode(pad(body)))


@pytest.fixture()
def srv(tmp_path, monkeypatch):
    monkeypatch.setenv("PROOF_LICENSE_DATA_DIR", str(tmp_path))
    from proof_license import app, keys, registry
    app.reset_cache()
    app._hits.clear()
    key = keys.generate()

    class S:
        c = TestClient(app.app)
        pub = keys.public_pem(key)
        reg = registry
        mod = app
        dir = tmp_path
    return S


def act(s, key, iid=IID, fp=FP):
    return s.c.post("/v1/activate", json={"key": key, "install_id": iid, "fingerprint": fp, "version": "1.0.0"})


def test_health_and_public_key(srv):
    assert srv.c.get("/healthz").json()["status"] == "ok"
    pk = srv.c.get("/v1/public-key").json()
    assert pk["alg"] == "Ed25519" and pk["pem"] == srv.pub and len(pk["kid"]) == 16


def test_validate_summary(srv):
    key, rec = srv.reg.issue("pro", "Acme Corp", seats=5, max_installs=2, days=365)
    v = srv.c.post("/v1/validate", json={"key": key}).json()
    assert v["status"] == "valid" and v["tier"] == "pro" and v["licensed_to"] == "Acme Corp"
    assert v["seats"] == 5 and v["installs_used"] == 0 and v["installs_max"] == 2
    assert v["key_masked"].endswith(key[-4:]) and key not in json.dumps(v)


def test_key_normalization(srv):
    key, _ = srv.reg.issue("free", "Solo")
    assert srv.c.post("/v1/validate", json={"key": key.lower().replace("-", " ")}).status_code == 200


def test_unknown_expired_revoked(srv):
    r = srv.c.post("/v1/validate", json={"key": "PCL-0000-0000-0000-0000"})
    assert r.status_code == 404 and r.json()["detail"] == "Invalid license key"
    key, rec = srv.reg.issue("pro", "Lapsed", days=1)
    with srv.reg.connect() as c:
        c.execute("UPDATE license_key SET expires_at='2020-01-01T00:00:00Z' WHERE id=?", (rec["id"],))
    assert srv.c.post("/v1/validate", json={"key": key}).status_code == 403
    key2, rec2 = srv.reg.issue("pro", "Gone")
    srv.reg.set_key_status(rec2["id"], "revoked")
    r = srv.c.post("/v1/validate", json={"key": key2})
    assert r.status_code == 403 and "revoked" in r.json()["detail"].lower()


def test_activate_token_claims_pro(srv):
    key, rec = srv.reg.issue("pro", "Acme Corp", seats=5, days=365)
    r = act(srv, key)
    assert r.status_code == 200 and r.json()["status"] == "active"
    c = verify_v1(r.json()["token"], srv.pub)
    assert c["install_id"] == IID and c["fingerprint"] == FP and c["tier"] == "pro"
    assert c["lic"] == rec["id"] and c["seats"] == 5 and c["refresh_by"] and c["expires_at"]
    assert c["offline"] is False and c["iss"] == "proofcontroller"


def test_free_token_has_no_refresh(srv):
    key, _ = srv.reg.issue("free", "Hobbyist")
    c = verify_v1(act(srv, key).json()["token"], srv.pub)
    assert c["refresh_by"] is None and c["expires_at"] is None


def test_install_limit_and_deactivate(srv):
    key, rec = srv.reg.issue("pro", "One Box", max_installs=1)
    assert act(srv, key).status_code == 200
    assert act(srv, key).status_code == 200  # same install re-activates
    r = act(srv, key, iid="inst_" + "b" * 32)
    assert r.status_code == 409 and "Install limit" in r.json()["detail"]
    assert srv.c.post("/v1/deactivate", json={"install_id": IID, "fingerprint": FP}).json()["status"] == "deactivated"
    assert srv.reg.active_installs(rec["id"]) == 0
    assert act(srv, key, iid="inst_" + "b" * 32).status_code == 200


def test_refresh(srv):
    key, rec = srv.reg.issue("max", "Big Co")
    act(srv, key)
    r = srv.c.post("/v1/refresh", json={"install_id": IID, "fingerprint": FP})
    assert r.status_code == 200 and verify_v1(r.json()["token"], srv.pub)["tier"] == "max"
    # wrong host
    assert srv.c.post("/v1/refresh", json={"install_id": IID, "fingerprint": "e" * 64}).status_code == 403
    # unknown install
    assert srv.c.post("/v1/refresh", json={"install_id": "inst_" + "c" * 32, "fingerprint": FP}).status_code == 404
    # revoked
    srv.reg.set_key_status(rec["id"], "revoked")
    assert srv.c.post("/v1/refresh", json={"install_id": IID, "fingerprint": FP}).status_code == 403
    # deactivated install cannot refresh
    srv.reg.set_key_status(rec["id"], "active")
    srv.c.post("/v1/deactivate", json={"install_id": IID, "fingerprint": FP})
    r = srv.c.post("/v1/refresh", json={"install_id": IID, "fingerprint": FP})
    assert r.status_code == 403 and "not active" in r.json()["detail"]


def test_offline_gov_file(srv, tmp_path):
    from proof_license import cli
    key, _ = srv.reg.issue("gov", "Agency", days=730)
    out = tmp_path / "gov.license"
    assert cli.main(["offline", "--key", key, "--install-id", IID, "--fingerprint", FP,
                     "--days", "365", "--out", str(out)]) == 0
    c = verify_v1(out.read_text().strip(), srv.pub)
    assert c["tier"] == "gov" and c["offline"] is True and c["refresh_by"] is None and c["expires_at"]


def test_cli_issue_json(srv, capsys):
    from proof_license import cli
    assert cli.main(["issue", "--tier", "pro", "--to", "CLI Co", "--seats", "3", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["key"].startswith("PCL-") and out["seats"] == 3
    assert srv.reg.find_key(out["key"])["licensed_to"] == "CLI Co"


def test_init_refuses_overwrite(srv):
    from proof_license import cli
    assert cli.main(["init"]) == 1


def test_no_plaintext_key_stored(srv):
    key, _ = srv.reg.issue("pro", "Hash Only")
    raw = (srv.dir / "registry.db").read_bytes()
    assert key.encode() not in raw and key.replace("-", "").encode() not in raw


def test_signing_key_mode(srv):
    assert (srv.dir / "signing_key.pem").stat().st_mode & 0o777 == 0o600


def test_rate_limit(srv):
    for _ in range(srv.mod.RATE_MAX):
        srv.c.post("/v1/validate", json={"key": "PCL-0000-0000-0000-0000"})
    assert srv.c.post("/v1/validate", json={"key": "PCL-0000-0000-0000-0000"}).status_code == 429
