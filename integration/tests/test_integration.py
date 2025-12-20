"""Phase 5 integration tests for the unified system."""

from __future__ import annotations

import json
import os
import time
import unittest
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


def _request_json(url: str, timeout: int = 5) -> Dict[str, Any]:
    """Fetch JSON from a URL and return the decoded payload."""
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        body = response.read().decode("utf-8")
        if "application/json" not in content_type:
            raise AssertionError(f"Expected JSON response from {url}")
        return json.loads(body)


def _wait_for_url(url: str, timeout: int = 10) -> None:
    """Wait for a URL to respond with HTTP 200 within a timeout."""
    start = time.time()
    last_error: Optional[Exception] = None
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except Exception as exc:
            last_error = exc
        time.sleep(0.5)
    if last_error:
        raise last_error
    raise TimeoutError(f"Timed out waiting for {url}")


class TestUnifiedIntegration(unittest.TestCase):
    """Validate that the unified system is serving key endpoints."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.base_url = os.getenv("UNIFIED_API_BASE_URL", "http://localhost:8080").rstrip("/")
        _wait_for_url(f"{cls.base_url}/")

    def test_gateway_root(self) -> None:
        """Ensure the gateway serves the frontend shell."""
        with urllib.request.urlopen(f"{self.base_url}/", timeout=5) as response:
            body = response.read().decode("utf-8")
        self.assertIn("<html", body.lower())

    def test_graphical_health(self) -> None:
        """Graphical-model health endpoint via gateway."""
        payload = _request_json(f"{self.base_url}/api/graphical/health")
        self.assertIn(payload.get("status"), {"ok", "healthy"})

    def test_tagger_health(self) -> None:
        """Image-tagger health endpoint via gateway."""
        payload = _request_json(f"{self.base_url}/api/tagger/health")
        self.assertIn(payload.get("status"), {"ok", "healthy"})

    def test_article_health(self) -> None:
        """Article-eater health endpoint via gateway."""
        payload = _request_json(f"{self.base_url}/api/article/health")
        self.assertEqual(payload.get("status"), "ok")

    def test_graph_health(self) -> None:
        """Knowledge-graph health endpoint via gateway."""
        payload = _request_json(f"{self.base_url}/api/graph/health")
        self.assertEqual(payload.get("status"), "ok")


if __name__ == "__main__":
    unittest.main()
