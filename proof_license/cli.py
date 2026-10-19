"""proof-license: operator CLI for the license server.

    proof-license init                      create the signing key, print the public key
    proof-license pubkey                    print the public key (ship it in the controller)
    proof-license issue --tier pro --to "Acme Corp" [--seats 5] [--installs 1]
                        [--email a@b.com] [--days 365]
    proof-license list                      keys, tier, installs used / max, status
    proof-license revoke  lic_...           refresh and activate stop working
    proof-license restore lic_...
    proof-license offline --key PCL-... --install-id ... --fingerprint ... [--days 365]
                                            signed Gov license file for an air-gapped host
    proof-license serve [--host 127.0.0.1] [--port 8443]
"""

from __future__ import annotations

import argparse
import json
import sys

from . import keys, registry, settings


def _print_table(rows: list[dict]) -> None:
    if not rows:
        print("no keys")
        return
    cols = ["id", "tier", "licensed_to", "seats", "active_installs", "max_installs", "expires_at", "status", "last_four"]
    print("\t".join(cols))
    for r in rows:
        print("\t".join(str(r.get(c) if r.get(c) is not None else "-") for c in cols))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="proof-license", description="Proof Controller license server admin")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create the signing key")
    sub.add_parser("pubkey", help="print the public key PEM")

    i = sub.add_parser("issue", help="issue a license key")
    i.add_argument("--tier", required=True, choices=settings.TIERS)
    i.add_argument("--to", required=True, dest="licensed_to", help="licensee name shown on the License screen")
    i.add_argument("--seats", type=int, default=1)
    i.add_argument("--installs", type=int, default=1, help="how many hosts may activate this key")
    i.add_argument("--email")
    i.add_argument("--days", type=int, help="key expiry in days; omit for no expiry")
    i.add_argument("--json", action="store_true")

    sub.add_parser("list", help="list keys")
    for name in ("revoke", "restore"):
        s = sub.add_parser(name)
        s.add_argument("key_id")

    o = sub.add_parser("offline", help="sign an offline (Gov) license file")
    o.add_argument("--key", required=True)
    o.add_argument("--install-id", required=True)
    o.add_argument("--fingerprint", required=True)
    o.add_argument("--days", type=int, default=365)
    o.add_argument("--out", help="write to this file instead of stdout")

    s = sub.add_parser("serve", help="run the HTTP server (put TLS in front of it)")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8443)

    a = p.parse_args(argv)

    if a.cmd == "init":
        try:
            key = keys.generate()
        except FileExistsError as e:
            print(str(e), file=sys.stderr)
            return 1
        print(f"signing key written to {settings.signing_key_path()} (mode 0600). Back it up offline.")
        print("public key (commit as proof_controller/license_pubkey.pem):")
        print(keys.public_pem(key), end="")
        return 0

    if a.cmd == "pubkey":
        print(keys.public_pem(keys.load_signing_key()), end="")
        return 0

    if a.cmd == "issue":
        key, rec = registry.issue(a.tier, a.licensed_to, seats=a.seats, max_installs=a.installs,
                                  email=a.email, days=a.days)
        out = {k: rec[k] for k in ("id", "tier", "licensed_to", "seats", "max_installs", "expires_at")}
        out["key"] = key
        if a.json:
            print(json.dumps(out))
        else:
            print(f"key:      {key}")
            print("          shown once; only its hash is stored. Email it to the customer now.")
            for k in ("id", "tier", "licensed_to", "seats", "max_installs", "expires_at"):
                print(f"{k + ':':<10}{out[k] if out[k] is not None else 'never'}")
        return 0

    if a.cmd == "list":
        _print_table(registry.list_keys())
        return 0

    if a.cmd in ("revoke", "restore"):
        ok = registry.set_key_status(a.key_id, "revoked" if a.cmd == "revoke" else "active")
        print(f"{a.key_id}: {'revoked' if a.cmd == 'revoke' else 'active'}" if ok else f"no such key {a.key_id}")
        return 0 if ok else 1

    if a.cmd == "offline":
        from .app import issue_token
        rec = registry.find_key(a.key)
        problem = registry.key_problem(rec)
        if problem:
            print(problem, file=sys.stderr)
            return 1
        registry.bind(rec["id"], a.install_id, a.fingerprint, None)
        tok = issue_token(rec, a.install_id, a.fingerprint, offline=True, days=a.days)
        if a.out:
            with open(a.out, "w", encoding="ascii") as fh:
                fh.write(tok + "\n")
            print(f"wrote {a.out}")
        else:
            print(tok)
        return 0

    if a.cmd == "serve":
        import uvicorn
        uvicorn.run("proof_license.app:app", host=a.host, port=a.port, log_level="info",
                    proxy_headers=True, forwarded_allow_ips="127.0.0.1")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
