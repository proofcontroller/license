# Proof Controller license server

Issues Proof Controller license keys, binds them to installs, and returns signed license tokens. Installed controllers (`proofcontroller/open`) verify those tokens offline with the public key shipped in their package, so the controller keeps running if this server is down.

Runs at `https://license.proofcontroller.com`. The controller's default `PROOF_CONTROLLER_LICENSE_SERVER` already points there.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/healthz` | Liveness |
| GET | `/v1/public-key` | Public key PEM and key id |
| POST | `/v1/validate` | `{key}` -> summary (tier, licensed to, seats, expiry, installs used/max). No state change |
| POST | `/v1/activate` | `{key, install_id, fingerprint, version}` -> signed token; binds the install |
| POST | `/v1/refresh` | `{install_id, fingerprint}` -> new token, or 403 if revoked/expired/deactivated |
| POST | `/v1/deactivate` | `{install_id, fingerprint}` -> frees the install slot |

Errors: `404` unknown key or install, `403` revoked, expired, or wrong host, `409` install limit reached, `429` rate limited (30 requests per minute per client on key routes).

## Token format (v1)

```
v1.<base64url(JSON claims, sorted keys)>.<base64url(Ed25519 signature over "v1.<payload>")>
```

Claims: `iss`, `kid`, `lic`, `install_id`, `fingerprint`, `tier` (free, pro, max, gov), `seats`, `licensed_to`, `issued_at`, `expires_at` (null = never), `refresh_by` (null for free, gov, and offline files; now + 7 days for pro and max), `offline`.

`tests/test_server.py` holds the reference verifier. Change the format only together with `proof_controller/licensing.py` in `proofcontroller/open`.

## Develop

```
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

Run it against a local controller:

```
export PROOF_LICENSE_DATA_DIR=$PWD/.license-dev
proof-license init && proof-license pubkey > .license-dev/pub.pem
proof-license issue --tier pro --to "Dev" --days 30       # prints a key
proof-license serve --port 8443
# in ../open:
PROOF_CONTROLLER_LICENSE_SERVER=http://127.0.0.1:8443 \
PROOF_CONTROLLER_LICENSE_PUBKEY=../license/.license-dev/pub.pem \
PROOF_CONTROLLER_STATE_DIR=$PWD/.state python3 -m proof_controller.cli
# open http://localhost:5150/license and paste the key
```

# Deploy to license.proofcontroller.com

One EC2 t3.micro (free tier), Ubuntu 24.04, HTTPS 443 via Caddy. About 20 minutes.

The server holds the license registry (SQLite) and the license signing key. It never receives arena data, proof bundles, or customer cloud credentials.

## 1. Launch the instance

1. EC2 > Launch instance: Ubuntu Server 24.04, `t3.micro`, your key pair.
2. Security group inbound: 22 from your IP only, 80 and 443 from anywhere (80 is only for the certificate challenge).
3. Elastic IP: allocate one and associate it, so the address survives restarts.
4. DNS: add an A record `license.proofcontroller.com` pointing at the Elastic IP.

## 2. Install

```
ssh ubuntu@license.proofcontroller.com
sudo apt-get update && sudo apt-get install -y python3-venv git gh caddy
sudo adduser --system --group --no-create-home prooflic
gh repo clone proofcontroller/license /tmp/license   # gh auth login as proofcontroller first
sudo python3 -m venv /opt/proof-license/venv
sudo /opt/proof-license/venv/bin/pip install /tmp/license
sudo cp /tmp/license/deploy/proof-license.service /etc/systemd/system/
sudo cp /tmp/license/deploy/Caddyfile /etc/caddy/Caddyfile
```

## 3. Create the signing key (once, ever)

```
sudo mkdir -p /var/lib/proof-license && sudo chown prooflic:prooflic /var/lib/proof-license && sudo chmod 700 /var/lib/proof-license
sudo -u prooflic PROOF_LICENSE_DATA_DIR=/var/lib/proof-license /opt/proof-license/venv/bin/proof-license init
```

It prints the public key. Then:

- Commit that public key to `proofcontroller/open` as `proof_controller/license_pubkey.pem`. Every controller build ships it and verifies tokens with it. Until it is committed, activation answers `503 License public key is not installed in this build`.
- Back up `/var/lib/proof-license/signing_key.pem` somewhere offline (encrypted USB, password manager). If it is lost, every installed controller must be rebuilt with a new public key. If it leaks, anyone can mint licenses.

## 4. Start

```
sudo systemctl daemon-reload
sudo systemctl enable --now proof-license caddy
sudo systemctl reload caddy
curl https://license.proofcontroller.com/healthz
```

## 5. Issue keys

Run on the server as the service user. Alias it to save typing:

```
alias pl='sudo -u prooflic PROOF_LICENSE_DATA_DIR=/var/lib/proof-license /opt/proof-license/venv/bin/proof-license'

pl issue --tier free --to "Jane Doe"                                   # free, no expiry
pl issue --tier pro  --to "Acme Corp" --seats 5 --days 365 --email ops@acme.example
pl issue --tier max  --to "Big Co" --seats 25 --installs 3 --days 365
pl list
pl revoke lic_...        # next refresh fails; the controller drops to no license
pl restore lic_...
```

The key is printed once. Only its SHA-256 hash is stored, so email it to the customer right away.

`--installs` is how many hosts may activate the key (default 1). A customer moves hosts by clicking deactivate on the old one (`DELETE /api/v1/license`), which frees the slot.

## 6. Gov (air-gapped) license file

The customer runs this on the air-gapped host and sends you the two values:

```
curl -s http://localhost:5150/api/v1/license/identity
```

Then:

```
pl issue --tier gov --to "Agency" --days 730
pl offline --key PCL-... --install-id inst_... --fingerprint ... --days 365 --out agency.license
```

Send `agency.license` out of band. They load it on the License screen or with `POST /api/v1/license/file`. No outbound call ever.

## Backups and operations

- Back up `/var/lib/proof-license/registry.db` daily (`sqlite3 registry.db ".backup /path/registry-$(date +%F).db"`). Losing it does not stop installed controllers, but refresh starts failing and keys must be reissued.
- Logs: `journalctl -u proof-license -f`.
- Upgrade: `sudo /opt/proof-license/venv/bin/pip install --upgrade /tmp/license && sudo systemctl restart proof-license`.
- Planned: move the signing key into AWS KMS. Only `proof_license/keys.py` changes.

## License

Greater Good Commercial License 1.0 (GGL-C), see [LICENSE.md](LICENSE.md). This is the operator's server; it is not part of the open-core controller.

## Author

Craig Ellrod - ORCID [0009-0004-1058-7666](https://orcid.org/0009-0004-1058-7666)
