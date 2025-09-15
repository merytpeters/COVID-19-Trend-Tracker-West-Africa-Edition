import os
import json

cache_file = "covid_data_cache.json"


def cache_check():
    if not os.path.exists(cache_file):
        return {"error": "Cache not found. Please run /update-data first."}

    with open(cache_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)
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
