"""Data flow integration tests for backend pipelines.

These tests validate that endpoints return data conforming to the
schemas defined in contracts/*.schema.json.
"""

from __future__ import annotations

import json
import os
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

# Try to import jsonschema for validation; skip schema tests if unavailable
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


CONTRACTS_DIR = Path(__file__).resolve().parent.parent.parent / "contracts"


def _load_schema(name: str) -> Dict[str, Any]:
    """Load a JSON schema from the contracts directory."""
    schema_path = CONTRACTS_DIR / f"{name}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    with open(schema_path) as f:
        return json.load(f)


def _validate_against_schema(data: Any, schema_name: str) -> List[str]:
    """Validate data against a schema and return list of errors."""
    if not HAS_JSONSCHEMA:
        return []  # Skip validation if jsonschema not installed

    schema = _load_schema(schema_name)
    validator = jsonschema.Draft7Validator(schema)
    errors = []
    for error in validator.iter_errors(data):
        path = " -> ".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"{path}: {error.message}")
    return errors


def _request_json(
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 5,
) -> Dict[str, Any]:
    """Make an HTTP request and return JSON response."""
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


class TestContractSchemas(unittest.TestCase):
    """Validate that contract schema files exist and are valid JSON Schema."""

    def test_schemas_exist(self) -> None:
        """All expected schema files exist."""
        expected = [
            "evidence_export.schema.json",
            "training_data_export.schema.json",
            "graph_export.schema.json",
            "posteriors_update.schema.json",
        ]
        for schema_file in expected:
            path = CONTRACTS_DIR / schema_file
            self.assertTrue(path.exists(), f"Missing schema: {schema_file}")

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_schemas_are_valid(self) -> None:
        """All schemas are valid Draft-07 JSON Schema."""
        for schema_file in CONTRACTS_DIR.glob("*.schema.json"):
            with open(schema_file) as f:
                schema = json.load(f)
            # This will raise if the schema itself is invalid
            jsonschema.Draft7Validator.check_schema(schema)


class TestDataFlowEndpoints(unittest.TestCase):
    """Validate data flow endpoints defined in DATA_FLOW_INTEGRATION_PLAN.md."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.base_url = os.getenv("UNIFIED_API_BASE_URL", "http://localhost:8080").rstrip("/")

    def _assert_schema_valid(self, data: Any, schema_name: str) -> None:
        """Assert that data validates against the named schema."""
        if not HAS_JSONSCHEMA:
            self.skipTest("jsonschema not installed")
        errors = _validate_against_schema(data, schema_name)
        if errors:
            self.fail(f"Schema validation failed for {schema_name}:\n" + "\n".join(errors[:10]))

    # --- Phase 2: Article-Eater -> Knowledge-Graph ---

    def test_article_export_to_graph_returns_json(self) -> None:
        """Article-eater export endpoint returns JSON."""
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/article/integration/export-to-graph",
        )
        self.assertIsInstance(payload, (list, dict))

    def test_article_export_to_graph_schema(self) -> None:
        """Article-eater export conforms to evidence_export schema."""
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/article/integration/export-to-graph",
        )
        # Endpoint may return list directly or wrapped in dict
        data = payload if isinstance(payload, list) else payload.get("findings", [])
        self._assert_schema_valid(data, "evidence_export")

    def test_graph_update_from_findings_accepts_valid_payload(self) -> None:
        """Knowledge-graph accepts valid findings payload."""
        valid_finding = {
            "edge_id": "test-edge-001",
            "from_node": "V1-001",
            "to_node": "M01",
            "effect_direction": "positive",
            "effect_size": 0.35,
        }
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/graph/edges/update-from-findings",
            payload=[valid_finding],
        )
        self.assertIsInstance(payload, dict)
        # Should return confirmation of update
        self.assertIn("updated", payload)

    # --- Phase 3: Image-Tagger -> Graphical-Model ---

    def test_tagger_export_training_data_returns_json(self) -> None:
        """Image-tagger export endpoint returns JSON."""
        payload = _request_json(
            "GET",
            f"{self.base_url}/api/tagger/v1/export/bn-training-data",
        )
        self.assertIsInstance(payload, dict)

    def test_tagger_export_training_data_schema(self) -> None:
        """Image-tagger export conforms to training_data_export schema."""
        payload = _request_json(
            "GET",
            f"{self.base_url}/api/tagger/v1/export/bn-training-data",
        )
        self._assert_schema_valid(payload, "training_data_export")

    def test_tagger_export_has_required_fields(self) -> None:
        """Image-tagger export includes version and images array."""
        payload = _request_json(
            "GET",
            f"{self.base_url}/api/tagger/v1/export/bn-training-data",
        )
        self.assertIn("version", payload)
        self.assertIn("images", payload)
        self.assertIsInstance(payload["images"], list)

    def test_graphical_import_training_data_accepts_valid_payload(self) -> None:
        """Graphical-model import accepts valid training data."""
        valid_import = {
            "version": "1.0",
            "images": [
                {
                    "image_id": "test-img-001",
                    "attributes": {"wood_coverage": 0.3, "plant_density": 0.5},
                }
            ],
            "trigger_retrain": False,
        }
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/graphical/integration/import-training-data",
            payload=valid_import,
        )
        self.assertIsInstance(payload, dict)
        self.assertIn("imported", payload)

    # --- Phase 4: Knowledge-Graph <-> Graphical-Model ---

    def test_graph_export_for_bayesian_returns_json(self) -> None:
        """Knowledge-graph export endpoint returns JSON."""
        payload = _request_json(
            "GET",
            f"{self.base_url}/api/graph/export-for-bayesian",
        )
        self.assertIsInstance(payload, dict)

    def test_graph_export_for_bayesian_schema(self) -> None:
        """Knowledge-graph export conforms to graph_export schema."""
        payload = _request_json(
            "GET",
            f"{self.base_url}/api/graph/export-for-bayesian",
        )
        self._assert_schema_valid(payload, "graph_export")

    def test_graph_export_has_nodes_and_edges(self) -> None:
        """Knowledge-graph export includes nodes and edges arrays."""
        payload = _request_json(
            "GET",
            f"{self.base_url}/api/graph/export-for-bayesian",
        )
        self.assertIn("nodes", payload)
        self.assertIn("edges", payload)
        self.assertIsInstance(payload["nodes"], list)
        self.assertIsInstance(payload["edges"], list)

    def test_graphical_publish_posteriors(self) -> None:
        """Graphical-model can publish posteriors."""
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/graphical/integration/publish-posteriors",
            payload={"model_version": "test-v1"},
        )
        self.assertIsInstance(payload, dict)

    def test_graph_update_from_posteriors_accepts_valid_payload(self) -> None:
        """Knowledge-graph accepts valid posteriors update."""
        valid_posterior = {
            "edge_id": "test-edge-001",
            "posterior_mean": 0.42,
            "posterior_sd": 0.08,
            "credible_interval_95": [0.26, 0.58],
            "model_version": "test-v1",
        }
        payload = _request_json(
            "POST",
            f"{self.base_url}/api/graph/edges/update-from-posteriors",
            payload=[valid_posterior],
        )
        self.assertIsInstance(payload, dict)


class TestSchemaValidationHelpers(unittest.TestCase):
    """Test the schema validation helper functions."""

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_valid_evidence_export(self) -> None:
        """Valid evidence export data passes schema validation."""
        valid_data = [
            {
                "edge_id": "edge-001",
                "from_node": "V1-001",
                "to_node": "M01",
                "effect_direction": "positive",
                "effect_size": 0.35,
                "uncertainty": {"pi": 0.8, "gamma": 0.6},
            }
        ]
        errors = _validate_against_schema(valid_data, "evidence_export")
        self.assertEqual(errors, [])

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_invalid_evidence_export_missing_required(self) -> None:
        """Invalid evidence export (missing required field) fails validation."""
        invalid_data = [
            {
                "edge_id": "edge-001",
                # missing from_node, to_node, effect_direction
            }
        ]
        errors = _validate_against_schema(invalid_data, "evidence_export")
        self.assertGreater(len(errors), 0)

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_invalid_evidence_export_bad_enum(self) -> None:
        """Invalid evidence export (bad enum value) fails validation."""
        invalid_data = [
            {
                "edge_id": "edge-001",
                "from_node": "V1-001",
                "to_node": "M01",
                "effect_direction": "sideways",  # not a valid enum value
            }
        ]
        errors = _validate_against_schema(invalid_data, "evidence_export")
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("effect_direction" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
