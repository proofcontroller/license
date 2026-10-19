"""License signing key.

v1.0 keeps the Ed25519 private key in a 0600 PEM file on the license
server's disk. Moving custody to AWS KMS is the planned follow-up; only
load_signing_key() changes when that happens.

This key is distinct from any proof-signing key. Compromise of one does
not forge the other.
"""

from __future__ import annotations

import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from . import settings


def generate(path: Path | None = None) -> Ed25519PrivateKey:
    """Create a new signing key. Refuses to overwrite an existing one."""
    path = path or settings.signing_key_path()
    if path.exists():
        raise FileExistsError(f"signing key already exists at {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    key = Ed25519PrivateKey.generate()
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(pem)
    return key


def load_signing_key(path: Path | None = None) -> Ed25519PrivateKey:
    path = path or settings.signing_key_path()
    key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError("license signing key must be Ed25519")
    return key


def public_pem(key: Ed25519PrivateKey) -> str:
    return key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")
