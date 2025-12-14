from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint to ensure API is up."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "AI Interview API is running properly."}
