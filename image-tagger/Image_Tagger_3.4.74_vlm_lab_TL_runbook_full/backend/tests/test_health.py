"""
Health endpoint checks for Image Tagger backend.
"""

from fastapi.testclient import TestClient

from backend.main import app
from backend.versioning import VERSION


def test_health_endpoint_with_prefix() -> None:
    """Ensure the standardized prefix routes to the health endpoint."""
    client = TestClient(app)
    response = client.get("/api/v1/tagger/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["module"] == "image-tagger"
    assert data["version"] == VERSION
