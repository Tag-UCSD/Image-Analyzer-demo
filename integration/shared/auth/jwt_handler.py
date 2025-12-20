"""JWT handling utilities for shared authentication."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TokenData:
    """Decoded JWT token data."""

    user_id: str
    email: str
    role: str
    exp: int
    iat: int


@dataclass(frozen=True)
class UserIdentity:
    """Minimal user identity used for token creation."""

    user_id: str
    email: str
    role: str = "user"


def _base64url_encode(data: bytes) -> str:
    """Encode bytes to base64url without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _base64url_decode(data: str) -> bytes:
    """Decode base64url string (with or without padding)."""
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(message: bytes, secret: str) -> str:
    """Return base64url-encoded HMAC-SHA256 signature for a message."""
    digest = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).digest()
    return _base64url_encode(digest)


def create_access_token(
    user: UserIdentity,
    secret: str,
    expires_in_minutes: int = 60 * 24,
) -> str:
    """
    Create a signed JWT access token for the provided user.

    Args:
        user: User identity payload.
        secret: Secret key for HMAC signing.
        expires_in_minutes: Token lifespan in minutes.

    Returns:
        Signed JWT as a string.
    """
    issued_at = int(time.time())
    expires_at = issued_at + int(expires_in_minutes * 60)

    header = {"alg": "HS256", "typ": "JWT"}
    payload: Dict[str, Any] = {
        "sub": user.user_id,
        "email": user.email,
        "role": user.role,
        "iat": issued_at,
        "exp": expires_at,
    }

    header_b64 = _base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _base64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = _sign(signing_input, secret)

    return f"{header_b64}.{payload_b64}.{signature}"


def decode_token(token: str, secret: str) -> TokenData:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string.
        secret: Secret key for HMAC verification.

    Raises:
        ValueError: If token is malformed, invalid, or expired.

    Returns:
        TokenData with decoded fields.
    """
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Token must have header, payload, and signature")

    header_b64, payload_b64, signature = parts
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_signature = _sign(signing_input, secret)

    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Token signature is invalid")

    try:
        payload_raw = _base64url_decode(payload_b64)
        payload = json.loads(payload_raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Token payload is not valid JSON") from exc

    exp = payload.get("exp")
    if exp is None:
        raise ValueError("Token is missing expiration")

    if int(exp) < int(time.time()):
        raise ValueError("Token has expired")

    return TokenData(
        user_id=str(payload.get("sub", "")),
        email=str(payload.get("email", "")),
        role=str(payload.get("role", "user")),
        exp=int(exp),
        iat=int(payload.get("iat", 0)),
    )


def try_decode_token(token: str, secret: str) -> Optional[TokenData]:
    """
    Attempt to decode a JWT token and return None on failure.

    Args:
        token: JWT token string.
        secret: Secret key for HMAC verification.

    Returns:
        TokenData when valid, otherwise None.
    """
    try:
        return decode_token(token, secret)
    except ValueError:
        return None
