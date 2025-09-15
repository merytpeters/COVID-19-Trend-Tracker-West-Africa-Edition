"""Routes For Trend Tracker"""

from datetime import datetime, timedelta
from fastapi.routing import APIRouter
from fastapi import Query
from apps.services import fetcher
from apps.utils import helper


router = APIRouter()


@router.post("/update-data")
def update_data():
    """Run Fetch, Clean and Format services"""
    fetcher.get_covid_data()
    fetcher.filter_flatten_csv_data()
    fetcher.json_format()
    return {"status": "success", "message": "Data updated successfully."}


@router.get("/get-all-data")
def get_all_data():
    data = helper.cache_check()
    return data


@router.get("/filter")
def get_by_filter(keywords: list[str] = Query(...)):
    data = helper.cache_check()

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


@router.get("/timeseries")
def get_by_time(
    days: int = Query(
        ..., description="Number of days to filter, e.g., 30 for last 30 days"
    )
):
    """Filter by time duration"""
    data = helper.cache_check()

    if not data:
        return {"error": "Cache not found. Please run /update-data first."}

    cutoff_date = datetime.now() - timedelta(days=days)
    results = {}

    for country, records in data.items():
        matching_records = []

        if isinstance(records, list):
            for record in records:
                record_date_str = record.get("date")
                if not record_date_str:
                    continue
                try:
                    record_date = datetime.strptime(record_date_str, "%Y-%m-%d")
                    if record_date >= cutoff_date:
                        matching_records.append(record)
                except ValueError:
                    continue
        elif isinstance(records, dict):
            record_date_str = records.get("date")
            if record_date_str:
                try:
                    record_date = datetime.strptime(record_date_str, "%Y-%m-%d")
                    if record_date >= cutoff_date:
                        matching_records.append(records)
                except ValueError:
                    pass

        if matching_records:
            results[country] = matching_records

    if not results:
        return {"error": f"No records found in the last {days} days."}

    return results
