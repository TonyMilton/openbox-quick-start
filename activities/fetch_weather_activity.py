import os
import requests
from datetime import datetime
from temporalio import activity

@activity.defn
async def fetch_weather_activity(city: str) -> dict:
    api_key = os.environ["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return {
        "location": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "timestamp": datetime.utcnow().isoformat()
    }