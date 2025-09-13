"""Test for app entry point"""

from fastapi.testclient import TestClient
from server.apps.main import app


client = TestClient(app)


def test_home():
    """Test for welcome function"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_health():
    """Test for health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
