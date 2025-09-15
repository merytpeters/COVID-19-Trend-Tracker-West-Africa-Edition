"""Fetch Data from OpenDataSoft"""

import csv
import json
import requests


WEST_AFRICAN_COUNTRIES = [
    "Benin",
    "Burkina Faso",
    "Cape Verde",
    "Cote d'Ivoire",
    "Gambia",
    "Ghana",
    "Guinea",
    "Guinea-Bissau",
    "Liberia",
    "Mali",
    "Mauritania",
    "Niger",
    "Nigeria",
    "Senegal",
    "Sierra Leone",
    "Togo",
]


def get_covid_data():
    """Get Covid data from External API"""
    url = (
        "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
        "covid-19-pandemic-worldwide-data/exports/csv"
        "?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true"
    )

    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            with open("covid_data.csv", "wb") as file:
                file.write(response.content)
            print("Covid data downloaded and saved successfully.")
        else:
            print(f"Failed to retrieve file: Status code {response.status_code}")


def filter_flatten_csv_data():
    """Filter and Flatten data"""
    with (
        open("covid_data.csv", "r", encoding="utf-8") as infile,
        open("covid_data_clean.csv", "w", newline="") as outfile,
    ):
        reader = csv.DictReader(infile, delimiter=";")

        if reader.fieldnames is None:
            raise ValueError("CSV file is missing header row or is empty.")
        reader.fieldnames = [
            name.strip().lstrip("\ufeff") for name in reader.fieldnames
        ]
        print("Detected columns:", reader.fieldnames)

        fieldnames = list(reader.fieldnames)

        if "lat" not in fieldnames:
            fieldnames.append("lat")
        if "lon" not in fieldnames:
            fieldnames.append("lon")

        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for row in reader:
            if row["zone"] in WEST_AFRICAN_COUNTRIES:
                if row.get("location"):
                    parts = row["location"].split(",")
                    if len(parts) == 2:
                        row["lat"] = parts[0].strip()
                        row["lon"] = parts[1].strip()
                    else:
                        row["lat"] = ""
                        row["lon"] = ""
                else:
                    row["lat"] = ""
                    row["lon"] = ""

                print(row)
                writer.writerow(row)


def json_format():
    """Turn cleaned CSV into nested JSON by country"""
    data = {}
    with open("covid_data_clean.csv", "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter="\t")
        for row in reader:
            country = row["zone"]
            record = {
                "subzone": row.get("subzone"),
                "category": row["category"],
                "date": row["date"],
                "count": (
                    int(row["count"]) if row["count"].isdigit() else row["count"]
                ),
                "location": row["location"],
                "coordinates": {"lat": row["lat"], "lon": row["lon"]},
            }
            if country not in data:
                data[country] = []
            data[country].append(record)

    sorted_data = {}
    for country, records in data.items():
        sorted_data[country] = sorted(records, key=lambda x: x.get("date", ""))

    with open("covid_data_cache.json", "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

    print("covid_data_cache.json created successfully!")


if __name__ == "__main__":
    print("Downloading file...")
    get_covid_data()
    print("Download finished. Filtering now...")
    filter_flatten_csv_data()
    print("Filtering finished.")

    print("Done! Check covid_data_clean.csv")

    json_format()
    print("Data formatted to json")
