# Changelog

## 2026-10-19

- Adopted the Proof Protocol License 1.0 (LICENSE.md). Specifications: Apache-2.0. Software: proprietary.
- Added ETHICS.md (Proof Economy Code of Ethics).
- All prior versions of the specifications are relicensed under Apache-2.0 (see NOTICE.md).

All notable changes to this repository are recorded here.

## [1.0.0] - 2026-10-18

### Added
- License server (FastAPI): validate, activate, refresh, deactivate, public key, health.
- Key issue with hash-only storage (`PCL-XXXX-XXXX-XXXX-XXXX`, 80 random bits), install binding with per-key install limits, revoke and restore.
- Ed25519-signed v1 license tokens; Pro/Max refresh every 7 days, Free and Gov never.
- Offline Gov license files for air-gapped hosts.
- Per-client rate limit on key routes.
- `proof-license` admin CLI: init, pubkey, issue, list, revoke, restore, offline, serve.
- EC2 t3.micro + Caddy deploy files and guide.
- 14 tests (real key, real registry, reference token verifier).

Moved here from `proofcontroller/open` (`license_server/`), where it was first written.
