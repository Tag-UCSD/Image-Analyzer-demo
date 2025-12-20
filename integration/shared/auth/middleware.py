"""FastAPI authentication helpers for shared JWT handling."""

from __future__ import annotations

import os
from typing import Callable, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .jwt_handler import TokenData, decode_token


def get_secret_key() -> str:
    """Return the JWT secret key from environment or default."""
    return os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    secret: Optional[str] = None,
) -> TokenData:
    """
    Validate JWT credentials and return token data.

    Args:
        credentials: HTTP bearer credentials from FastAPI.
        secret: Optional override for secret key.

    Raises:
        HTTPException: When token is missing or invalid.

    Returns:
        TokenData for the authenticated user.
    """
    secret_key = secret or get_secret_key()

    try:
        return decode_token(credentials.credentials, secret_key)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


def require_role(required_role: str) -> Callable[[TokenData], TokenData]:
    """
    Return a dependency that enforces a minimum role requirement.

    Args:
        required_role: Role required to access the endpoint.

    Returns:
        Dependency function that validates the role.
    """
    def role_checker(user: TokenData = Depends(get_current_user)) -> TokenData:
        if user.role != required_role and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required",
            )
        return user

    return role_checker
