"""
Unit tests for main application.
"""
from fastapi.testclient import TestClient


def test_read_root(client: TestClient):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Interview API is running properly."}


def test_docs(client: TestClient):
    """Test that API documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200
