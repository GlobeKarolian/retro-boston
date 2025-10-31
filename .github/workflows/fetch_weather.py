
import json, os, sys, time
from datetime import datetime, timezone
import requests

# Simple: use fixed gridpoint for Boston area (NWS Boston/Taunton WFO BOX, gridpoint ~ 65,75)
FORECAST_URL = os.getenv("FORECAST_URL", "https://api.weather.gov/gridpoints/BOX/65,75/forecast")
OUTPUT = os.getenv("OUTPUT_PATH", "weather.json")

HEADERS = {
    "User-Agent": "retro-boston (github actions)",
    "Accept": "application/geo+json,application/json"
}

def main():
    r = requests.get(FORECAST_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    period = data["properties"]["periods"][0]
    out = {
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        "temperature": period.get("temperature"),
        "temperatureUnit": period.get("temperatureUnit", "F"),
        "shortForecast": period.get("shortForecast"),
        "name": period.get("name"),
        "detailedForecast": period.get("detailedForecast", ""),
    }
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("Wrote", OUTPUT, "->", out)

if __name__ == "__main__":
    main()
