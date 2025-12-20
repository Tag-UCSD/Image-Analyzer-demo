"""Tests for the unified API client."""

from __future__ import annotations

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from integration.shared.api_client import UnifiedAPIClient


class _TestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path == "/api/graphical/status":
            payload = {"status": "ok", "module": "graphical"}
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


class TestUnifiedAPIClient(unittest.TestCase):
    """Validate basic API client behavior."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = HTTPServer(("127.0.0.1", 0), _TestHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def test_graphical_status(self) -> None:
        client = UnifiedAPIClient(base_url=f"http://127.0.0.1:{self.port}")
        result = client.graphical_status()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["module"], "graphical")


if __name__ == "__main__":
    unittest.main()
