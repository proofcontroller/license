"""License server settings, from environment."""

from __future__ import annotations

import os
from pathlib import Path

TIERS = ("free", "pro", "max", "gov")


def data_dir() -> Path:
    return Path(os.environ.get("PROOF_LICENSE_DATA_DIR", "/var/lib/proof-license"))


def signing_key_path() -> Path:
    return Path(os.environ.get("PROOF_LICENSE_SIGNING_KEY", str(data_dir() / "signing_key.pem")))


def registry_path() -> Path:
    return Path(os.environ.get("PROOF_LICENSE_DB", str(data_dir() / "registry.db")))


# Pro / Max tokens must be refreshed online this often (spec 3.3, proposed default).
REFRESH_DAYS = int(os.environ.get("PROOF_LICENSE_REFRESH_DAYS", "7"))
