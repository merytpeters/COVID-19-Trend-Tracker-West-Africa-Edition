from datetime import datetime, timedelta
import os
import json


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

cache_file = os.path.join(PROJECT_ROOT, "covid_data_cache.json")


def cache_check():
    print(cache_file)
    if not os.path.exists(cache_file):
        return None

    with open(cache_file, "r", encoding="utf-8") as infile:
        try:
            data = json.load(infile)
        except json.JSONDecodeError:
            return None
    return data


def flatten_values(data):
    """Flatten all keys and all values
    (including digits) from nested dict/list
    into a list of lowercase strings.
    """
    values = []
    if isinstance(data, dict):
        for k, v in data.items():
            values.append(str(k).lower())
            if isinstance(v, (dict, list)):
                values.extend(flatten_values(v))
            else:
                values.append(str(v).lower())
    elif isinstance(data, list):
        for item in data:
            values.extend(flatten_values(item))
    else:
        values.append(str(data).lower())
    return values


def record_matches_keywords(record, keywords_lower):
    """Check if all keywords exist as substrings in the flattened record values."""
    record_values = flatten_values(record)
    return all(any(kw in value for value in record_values) for kw in keywords_lower)


def filter_by_time(data: dict, days: int):
    """Filter cached data by last N days."""
    cutoff_date = datetime.now() - timedelta(days=days)
    results = {}
    print(data)

    for country, records in data.items():
        matching_records = []

        if isinstance(records, list):
            for record in records:
                record_date_str = record.get("date")
                if not record_date_str:
                    continue
                try:

                    record_date = datetime.strptime(record_date_str[:10], "%Y-%m-%d")
                    if record_date >= cutoff_date:
                        matching_records.append(record)
                except ValueError:
                    continue
        elif isinstance(records, dict):
            record_date_str = records.get("date")
            if record_date_str:
                try:
                    record_date = datetime.strptime(record_date_str[:10], "%Y-%m-%d")
                    if record_date >= cutoff_date:
                        matching_records.append(records)
                except ValueError:
                    pass

        if matching_records:
            results[country] = matching_records

    return results
