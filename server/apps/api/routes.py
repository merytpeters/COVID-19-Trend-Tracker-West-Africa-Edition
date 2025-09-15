"""Routes For Trend Tracker"""

import json
import os
from fastapi.routing import APIRouter
from fastapi import Query
from apps.services import fetcher
from apps.utils import helper


router = APIRouter()
cache_file = "covid_data_cache.json"


@router.post("/update-data")
def update_data():
    """Run Fetch, Clean and Format services"""
    fetcher.get_covid_data()
    fetcher.filter_flatten_csv_data()
    fetcher.json_format()
    return {"status": "success", "message": "Data updated successfully."}


@router.get("/get-all-data")
def get_all_data():
    """Return cached COVID-19 data as JSON"""
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as infile:
            data = json.load(infile)
        return data
    return {"error": "Cache not found. Please run /update-data first."}


@router.get("/filter")
def get_by_filter(keywords: list[str] = Query(...)):
    """Get data by filter keywords with AND across country and record"""
    if not os.path.exists(cache_file):
        return {"error": "Cache not found. Please run /update-data first."}

    with open(cache_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    keywords_lower = [kw.lower() for kw in keywords]
    results = {}

    for country, records in data.items():
        matching_records = []

        country_lower = country.lower()

        remaining_keywords = [kw for kw in keywords_lower if kw not in country_lower]

        if isinstance(records, list):
            for record in records:
                if helper.record_matches_keywords(record, remaining_keywords):
                    matching_records.append(record)
        elif isinstance(records, dict):
            if helper.record_matches_keywords(records, remaining_keywords):
                matching_records.append(records)

        if matching_records:
            results[country] = matching_records

    if not results:
        return {"error": f"No records found containing all keywords: {keywords}"}

    return results
