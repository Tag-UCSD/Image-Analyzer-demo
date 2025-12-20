"""Unified API client for cross-module calls."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


class UnifiedAPIClient:
    """Minimal HTTP client for interacting with module APIs via the gateway."""

    def __init__(self, base_url: Optional[str] = None, timeout: int = 10) -> None:
        self.base_url = (base_url or os.getenv("UNIFIED_API_BASE_URL", "http://localhost:8080")).rstrip("/")
        self.timeout = timeout

    def request(
        self,
        path: str,
        method: str = "GET",
        payload: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Send an HTTP request and parse JSON responses when possible.

        Args:
            path: API path starting with '/'.
            method: HTTP method (GET, POST, etc.).
            payload: Optional JSON payload for requests with a body.

        Returns:
            Parsed JSON response or raw text.
        """
        url = urllib.parse.urljoin(f"{self.base_url}/", path.lstrip("/"))
        data = None
        headers = {"Accept": "application/json"}

        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(url, data=data, headers=headers, method=method.upper())

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return json.loads(body)
                return body
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8") if exc.fp else ""
            raise RuntimeError(
                f"Request failed ({exc.code}) for {url}: {error_body or exc.reason}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Unable to reach {url}: {exc.reason}") from exc

    def health(self, module: str) -> Any:
        """Check the health endpoint for a specific module."""
        return self.request(f"/api/{module}/health")

    def graphical_status(self) -> Any:
        """Retrieve graphical-model status."""
        return self.request("/api/graphical/status")

    def tagger_status(self) -> Any:
        """Retrieve image-tagger status."""
        return self.request("/api/tagger/status")

    def evidence_status(self) -> Any:
        """Retrieve article-eater status."""
        return self.request("/api/evidence/status")

    def graph_status(self) -> Any:
        """Retrieve knowledge-graph status."""
        return self.request("/api/graph/status")
