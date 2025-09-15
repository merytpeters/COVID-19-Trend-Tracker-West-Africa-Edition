from fastapi.testclient import TestClient
from server.apps.main import app

client = TestClient(app)


def test_update_data(monkeypatch):
    # Mock fetcher functions to avoid actual data fetching
    monkeypatch.setattr("server.apps.services.fetcher.get_covid_data", lambda: None)
    monkeypatch.setattr(
        "server.apps.services.fetcher.filter_flatten_csv_data", lambda: None
    )
    monkeypatch.setattr("server.apps.services.fetcher.json_format", lambda: None)
    response = client.post("/api/update-data")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_get_all_data(monkeypatch):
    mock_data = {"Nigeria": [{"date": "2023-01-01", "count": 1}]}
    monkeypatch.setattr("server.apps.utils.helper.cache_check", lambda: mock_data)
    response = client.get("/api/get-all-data")
    assert response.status_code == 200
    assert response.json() == mock_data


def test_get_by_filter_found(monkeypatch):
    mock_data = {
        "Nigeria": [
            {"date": "2023-01-01", "count": 1, "category": "Deaths", "subzone": "Lagos"}
        ]
    }
    monkeypatch.setattr("server.apps.utils.helper.cache_check", lambda: mock_data)
    monkeypatch.setattr(
        "server.apps.utils.helper.record_matches_keywords",
        lambda record, keywords: True,
    )
    response = client.get("/api/filter", params={"keywords": "Nigeria"})
    assert response.status_code == 200
    assert "Nigeria" in response.json()


def test_get_by_filter_not_found(monkeypatch):
    mock_data = {"Nigeria": []}
    monkeypatch.setattr("server.apps.utils.helper.cache_check", lambda: mock_data)
    monkeypatch.setattr(
        "server.apps.utils.helper.record_matches_keywords",
        lambda record, keywords: False,
    )
    response = client.get("/api/filter", params={"keywords": "Nonexistent"})
    assert response.status_code == 200
    assert "error" in response.json()


def test_get_by_time_found(monkeypatch):
    from datetime import datetime, timedelta

    today = datetime.now().strftime("%Y-%m-%d")
    mock_data = {
        "Nigeria": [
            {"date": today, "count": 1, "category": "Deaths", "subzone": "Lagos"}
        ]
    }
    monkeypatch.setattr("server.apps.utils.helper.cache_check", lambda: mock_data)
    response = client.get("/api/timeseries", params={"days": 1})
    assert response.status_code == 200
    assert "Nigeria" in response.json()


def test_get_by_time_not_found(monkeypatch):
    mock_data = {
        "Nigeria": [
            {"date": "2000-01-01", "count": 1, "category": "Deaths", "subzone": "Lagos"}
        ]
    }
    monkeypatch.setattr("server.apps.utils.helper.cache_check", lambda: mock_data)
    response = client.get("/api/timeseries", params={"days": 1})
    assert response.status_code == 200
    assert "error" in response.json()
