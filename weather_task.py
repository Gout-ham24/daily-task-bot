"""
BRONZE Task — Weather Fetcher
Fetches current weather for Thiruvananthapuram using OpenWeatherMap API.
"""

import os
import datetime
import requests


def get_weather_data() -> dict:
    api_key = os.environ["WEATHER_API_KEY"]
    city = os.getenv("CITY", "Thiruvananthapuram")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    raw = resp.json()

    weather = {
        "city": raw["name"],
        "country": raw["sys"]["country"],
        "description": raw["weather"][0]["description"].title(),
        "icon": raw["weather"][0]["icon"],
        "temp": round(raw["main"]["temp"], 1),
        "feels_like": round(raw["main"]["feels_like"], 1),
        "humidity": raw["main"]["humidity"],
        "wind_speed": round(raw["wind"]["speed"] * 3.6, 1),  # m/s → km/h
        "visibility": round(raw.get("visibility", 0) / 1000, 1),  # m → km
        "sunrise": datetime.datetime.fromtimestamp(raw["sys"]["sunrise"]).strftime("%I:%M %p"),
        "sunset": datetime.datetime.fromtimestamp(raw["sys"]["sunset"]).strftime("%I:%M %p"),
        "fetched_at": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p IST"),
    }

    return weather
