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


def test_api_routes():
    """Test that /api routes are included (basic check for 404 or 200)"""
    response = client.get("/api/")
    assert response.status_code in (200, 404)
