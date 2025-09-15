"""Routes For Trend Tracker"""

from fastapi.routing import APIRouter
from fastapi import Query
from server.apps.services import fetcher
from server.apps.utils import helper


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

    if not data:
        return {"error": "Cache not found. Please run /update-data first."}

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

    results = helper.filter_by_time(data, days)
    if not results:
        return {"error": f"No records found in the last {days} days."}

    return results


@router.get("/compare")
def compare_countries(countries: list[str] = Query(...), lastdays: int = Query(...)):
    """Compare countries data within a time period"""
    data = helper.cache_check()
    if not data:
        return {"error": "Cache not found. Please run /update-data first."}

    filtered_data = helper.filter_by_time(data, lastdays)
    if not filtered_data:
        return {"error": f"No records found in the last {lastdays} days."}

    result = {}
    filtered_countries_lower = {k.lower(): k for k in filtered_data.keys()}

    for c in countries:
        key_lower = c.lower()
        if key_lower in filtered_countries_lower:
            actual_key = filtered_countries_lower[key_lower]
            result[actual_key] = filtered_data[actual_key]

    if not result:
        return {
            "error": f"No records found for the given countries in the last {lastdays} days."
        }

    return result
