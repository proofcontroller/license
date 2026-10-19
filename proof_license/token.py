"""License token format, v1.

    v1.<payload>.<signature>

payload   = base64url(JSON, sorted keys, no whitespace), no padding
signature = base64url(Ed25519 signature over the ASCII bytes "v1.<payload>")

The controller verifies with the license server's public key, offline.
proof_controller/licensing.py implements the matching verifier.
"""

from __future__ import annotations

import base64
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

PREFIX = "v1"


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def sign(claims: dict, key: Ed25519PrivateKey) -> str:
    body = b64u(json.dumps(claims, sort_keys=True, separators=(",", ":")).encode())
    signing_input = f"{PREFIX}.{body}".encode("ascii")
    return f"{PREFIX}.{body}.{b64u(key.sign(signing_input))}"
