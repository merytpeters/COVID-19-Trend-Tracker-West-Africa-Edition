"""Test for Fetcher Service"""

import os
import csv
import pytest
from unittest import mock
from server.apps.services import fetcher


@pytest.fixture
def sample_csv(tmp_path):
    data = [
        {"zone": "Nigeria", "location": "9.082, 8.6753", "other": "data"},
        {"zone": "France", "location": "46.6034, 1.8883", "other": "data"},
        {"zone": "Ghana", "location": "", "other": "data"},
    ]
    csv_path = tmp_path / "covid_data.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["zone", "location", "other"], delimiter=";"
        )
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return csv_path


def test_filter_flatten_csv_data(tmp_path, sample_csv):
    # Copy sample_csv to working directory
    os.chdir(tmp_path)
    os.rename(sample_csv, "covid_data.csv")
    fetcher.filter_flatten_csv_data()
    # Check output file
    assert os.path.exists("covid_data_clean.csv")
    with open("covid_data_clean.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")  # Match fetcher output delimiter
        rows = list(reader)
        # Only Nigeria and Ghana should be present
        zones = [row["zone"] for row in rows]
        assert "Nigeria" in zones
        assert "Ghana" in zones
        assert "France" not in zones
        # Nigeria should have lat/lon filled, Ghana should be empty
        for row in rows:
            if row["zone"] == "Nigeria":
                assert row["lat"] == "9.082"
                assert row["lon"] == "8.6753"
            if row["zone"] == "Ghana":
                assert row["lat"] == ""
                assert row["lon"] == ""


@mock.patch("server.apps.services.fetcher.requests.get")
def test_get_covid_data_success(mock_get, tmp_path):
    # Mock a successful response
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.content = b"test,data\n1,2"
    mock_get.return_value.__enter__.return_value = mock_response
    os.chdir(tmp_path)
    fetcher.get_covid_data()
    assert os.path.exists("covid_data.csv")
    with open("covid_data.csv", "rb") as f:
        content = f.read()
        assert content == b"test,data\n1,2"


@mock.patch("server.apps.services.fetcher.requests.get")
def test_get_covid_data_failure(mock_get, capsys):
    # Mock a failed response
    mock_response = mock.Mock()
    mock_response.status_code = 404
    mock_get.return_value.__enter__.return_value = mock_response
    fetcher.get_covid_data()
    captured = capsys.readouterr()
    assert "Failed to retrieve file" in captured.out


def test_json_format(tmp_path):
    # Prepare a sample covid_data_clean.csv
    os.chdir(tmp_path)
    sample_rows = [
        {
            "zone": "Nigeria",
            "subzone": "Lagos",
            "category": "Confirmed",
            "date": "2022-01-01",
            "count": "100",
            "location": "9.082, 8.6753",
            "lat": "9.082",
            "lon": "8.6753",
        },
        {
            "zone": "Nigeria",
            "subzone": "Abuja",
            "category": "Confirmed",
            "date": "2022-01-02",
            "count": "50",
            "location": "9.0765, 7.3986",
            "lat": "9.0765",
            "lon": "7.3986",
        },
        {
            "zone": "Ghana",
            "subzone": "Accra",
            "category": "Confirmed",
            "date": "2022-01-01",
            "count": "30",
            "location": "5.6037, -0.1870",
            "lat": "5.6037",
            "lon": "-0.1870",
        },
    ]
    with open("covid_data_clean.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sample_rows[0].keys(), delimiter="\t")
        writer.writeheader()
        for row in sample_rows:
            writer.writerow(row)
    # Run json_format
    fetcher.json_format()
    # Check output file
    assert os.path.exists("covid_data_cache.json")
    import json

    with open("covid_data_cache.json", encoding="utf-8") as f:
        data = json.load(f)
        assert "Nigeria" in data
        assert "Ghana" in data
        assert isinstance(data["Nigeria"], list)
        assert data["Nigeria"][0]["category"] == "Confirmed"
        assert data["Nigeria"][0]["coordinates"]["lat"] == "9.082"
        assert data["Ghana"][0]["coordinates"]["lon"] == "-0.1870"
