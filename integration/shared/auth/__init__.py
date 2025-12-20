"""Shared auth helper exports."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from typing import Any


def _load_module(name: str, path: Path) -> Any:
    """Load a module from an explicit file path."""
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_auth_file = Path(__file__).resolve().parent.parent / "auth.py"
_auth_module = _load_module("integration_shared_auth_shim", _auth_file)

TokenData = _auth_module.TokenData
UserIdentity = _auth_module.UserIdentity
create_access_token = _auth_module.create_access_token
decode_token = _auth_module.decode_token
try_decode_token = _auth_module.try_decode_token
get_current_user = _auth_module.get_current_user
require_role = _auth_module.require_role

__all__ = [
    "TokenData",
    "UserIdentity",
    "create_access_token",
    "decode_token",
    "try_decode_token",
    "get_current_user",
    "require_role",
]
