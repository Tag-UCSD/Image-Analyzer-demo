"""Tests for shared auth helpers."""

from __future__ import annotations

import unittest

from integration.shared import auth


class TestAuth(unittest.TestCase):
    """Validate JWT helper behavior."""

    def test_create_and_decode_token(self) -> None:
        secret = "unit-test-secret"
        user = auth.UserIdentity(user_id="user-123", email="user@example.com", role="researcher")
        token = auth.create_access_token(user, secret, expires_in_minutes=5)
        decoded = auth.decode_token(token, secret)

        self.assertEqual(decoded.user_id, "user-123")
        self.assertEqual(decoded.email, "user@example.com")
        self.assertEqual(decoded.role, "researcher")
        self.assertGreater(decoded.exp, decoded.iat)

    def test_expired_token_raises(self) -> None:
        secret = "unit-test-secret"
        user = auth.UserIdentity(user_id="user-123", email="user@example.com", role="researcher")
        token = auth.create_access_token(user, secret, expires_in_minutes=-1)

        with self.assertRaises(ValueError):
            auth.decode_token(token, secret)


if __name__ == "__main__":
    unittest.main()
