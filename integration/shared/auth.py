"""Compatibility wrapper exposing shared auth helpers for gate checks."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from typing import Any, Callable

_AUTH_DIR = Path(__file__).resolve().parent / "auth"


def _load_module(name: str, path: Path) -> Any:
    """Load a module from an explicit file path."""
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_jwt_module = _load_module("integration_shared_auth_jwt", _AUTH_DIR / "jwt_handler.py")
TokenData = _jwt_module.TokenData
UserIdentity = _jwt_module.UserIdentity
create_access_token = _jwt_module.create_access_token
decode_token = _jwt_module.decode_token
try_decode_token = _jwt_module.try_decode_token

_middleware_module = None


def _load_middleware() -> Any:
    """Lazy-load FastAPI middleware helpers."""
    global _middleware_module
    if _middleware_module is None:
        _middleware_module = _load_module(
            "integration_shared_auth_middleware",
            _AUTH_DIR / "middleware.py",
        )
    return _middleware_module


def get_current_user(*args: Any, **kwargs: Any) -> Any:
    """Proxy to shared get_current_user, loaded lazily."""
    module = _load_middleware()
    return module.get_current_user(*args, **kwargs)


def require_role(*args: Any, **kwargs: Any) -> Callable[..., Any]:
    """Proxy to shared require_role, loaded lazily."""
    module = _load_middleware()
    return module.require_role(*args, **kwargs)

__all__ = [
    "TokenData",
    "UserIdentity",
    "create_access_token",
    "decode_token",
    "try_decode_token",
    "get_current_user",
    "require_role",
]
