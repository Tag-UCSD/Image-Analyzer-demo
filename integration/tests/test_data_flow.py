"""Data flow integration tests for backend pipelines."""

from __future__ import annotations

import json
import os
import unittest
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


def _request_json(
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 5,
) -> Dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        body = response.read().decode("utf-8")
        if "application/json" not in content_type:
            raise AssertionError(f"Expected JSON response from {url}")
        return json.loads(body)


class TestDataFlowEndpoints(unittest.TestCase):
    """Validate data flow endpoints defined in DATA_FLOW_INTEGRATION_PLAN.md."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.base_url = os.getenv("UNIFIED_API_BASE_URL", "http://localhost:8080").rstrip("/")

    def test_article_export_to_graph(self) -> None:
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/article/integration/export-to-graph",
        )
        self.assertIsInstance(payload, (list, dict))

    def test_graph_update_from_findings(self) -> None:
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/graph/edges/update-from-findings",
            payload=[],
        )
        self.assertIsInstance(payload, dict)

    def test_tagger_export_training_data(self) -> None:
        payload = _request_json(
            "GET",
            f"{self.base_url}/api/tagger/v1/export/bn-training-data",
        )
        self.assertIsInstance(payload, dict)

    def test_graphical_import_training_data(self) -> None:
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/graphical/integration/import-training-data",
            payload={"images": [], "trigger_retrain": False},
        )
        self.assertIsInstance(payload, dict)

    def test_graph_export_for_bayesian(self) -> None:
        payload = _request_json(
            "GET",
            f"{self.base_url}/api/graph/export-for-bayesian",
        )
        self.assertIsInstance(payload, dict)

    def test_graphical_publish_posteriors(self) -> None:
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/graphical/integration/publish-posteriors",
            payload={"model_version": "latest"},
        )
        self.assertIsInstance(payload, dict)

    def test_graph_update_from_posteriors(self) -> None:
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/graph/edges/update-from-posteriors",
            payload=[],
        )
        self.assertIsInstance(payload, dict)


if __name__ == "__main__":
    unittest.main()
