import requests
import csv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json

cities = {
    # lat, lon
    "New York City": [40.7128, -74.0060],
    "Los Angeles": [34.0522, -118.2437],
    "Chicago": [41.8781, -87.6298],
    "San Jose": [37.3361, -121.8906],
    "Houston": [29.7604, -95.3698],
    "Miami": [25.7617, -80.1918],
    "San Francisco": [37.7749, -122.4194],
    "Seattle": [47.6062, -122.3321],
    "Dallas": [32.7767, -96.7970]
}


def cloud_type(percent):
    if percent < 5:
        return "clear"
    if percent < 10:
        return "mostly clear"
    if percent < 25:
        return "slightly cloudy"
    if percent < 50:
        return "partly cloudy"
    if percent < 75:
        return "mostly cloudy"
    return "overcast"


def save_data(loc):
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": cities[loc][0],
        "longitude": cities[loc][1],
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "America/Los_Angeles",
        "temperature_unit": "fahrenheit",
        "start_date": (
            datetime.now(ZoneInfo("America/Los_Angeles")) - timedelta(days=366)
        ).strftime("%Y-%m-%d"),
        "end_date": (
            datetime.now(ZoneInfo("America/Los_Angeles")) - timedelta(days=1)
        ).strftime("%Y-%m-%d"),
    }
    print(params)
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    cleaned = data["daily"]

    with open("weather.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "temp_min", "temp_max"])
        writer.writerows(
            zip(
                cleaned["time"],
                cleaned["temperature_2m_max"],
                cleaned["temperature_2m_min"],
            )
        )

    current_weather(loc)


def current_weather(loc):
    url = "https://api.open-meteo.com/v1/gfs"

    params = {
        "latitude": cities[loc][0],
        "longitude": cities[loc][1],
        "current": (
            "temperature_2m,"
            "wind_speed_10m,"
            "wind_direction_10m,"
            "wind_gusts_10m,"
            "cloud_cover,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain,"
            "showers,"
            "snowfall,"
            "surface_pressure"
        ),
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "forecast_days": 1,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    result = {
        "city": loc,
        "latitude": cities[loc][0],
        "longitude": cities[loc][1],
        "current": data["current"],
        "current_units": data.get("current_units", {}),
    }

    filename = "weather.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    return result


weather = current_weather("Los Angeles")
