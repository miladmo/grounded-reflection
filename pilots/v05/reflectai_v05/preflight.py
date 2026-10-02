"""Live preflight checks that must pass before any reservation or key access."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

from .config import RunConfig


def verify_executable(config: RunConfig) -> None:
    path = Path(os.path.expandvars(config.pwsh_executable or ''))
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != config.pwsh_sha256:
        raise PermissionError('the pinned PowerShell 7 executable is missing or differs from its SHA-256')
