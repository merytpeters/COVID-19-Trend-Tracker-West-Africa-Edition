import json
import pytest
from datetime import datetime, timedelta
from server.apps.utils import helper


@pytest.fixture
def sample_cache_file(tmp_path):
    cache_path = tmp_path / "covid_data_cache.json"
    data = {"foo": "bar", "nested": {"num": 42}}
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return cache_path, data


def test_cache_check_found(sample_cache_file, monkeypatch):
    cache_path, expected_data = sample_cache_file
    monkeypatch.setattr(helper, "cache_file", str(cache_path))
    result = helper.cache_check()
    assert result == expected_data


def test_cache_check_not_found(tmp_path, monkeypatch):
    cache_path = tmp_path / "covid_data_cache.json"
    monkeypatch.setattr(helper, "cache_file", str(cache_path))
    result = helper.cache_check()
    assert result is None


def test_flatten_values_dict():
    data = {"A": 1, "B": {"C": 2, "D": [3, "X"]}}
    flat = helper.flatten_values(data)
    assert "a" in flat
    assert "1" in flat
    assert "c" in flat
    assert "2" in flat
    assert "3" in flat
    assert "x" in flat


def test_flatten_values_list():
    data = [1, {"A": 2}, [3, 4]]
    flat = helper.flatten_values(data)
    assert "1" in flat
    assert "a" in flat
    assert "2" in flat
    assert "3" in flat
    assert "4" in flat


def test_record_matches_keywords_true():
    record = {"name": "Alice", "info": {"city": "Lagos", "age": 30}}
    keywords = ["alice", "lag"]
    assert helper.record_matches_keywords(record, keywords)


def test_record_matches_keywords_false():
    record = {"name": "Alice", "info": {"city": "Lagos", "age": 30}}
    keywords = ["alice", "paris"]
    assert not helper.record_matches_keywords(record, keywords)


def test_filter_by_time_found():
    today = datetime.now().strftime("%Y-%m-%d")
    data = {
        "Nigeria": [
            {"date": today, "count": 1, "category": "Deaths", "subzone": "Lagos"}
        ]
    }
    result = helper.filter_by_time(data, days=1)
    assert "Nigeria" in result
    assert result["Nigeria"][0]["date"] == today


def test_filter_by_time_not_found():
    old_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    data = {
        "Nigeria": [
            {"date": old_date, "count": 1, "category": "Deaths", "subzone": "Lagos"}
        ]
    }
    result = helper.filter_by_time(data, days=1)
    assert result == {}
