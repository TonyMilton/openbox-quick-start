import os
import httpx
from temporalio import activity
from db import get_db_session, WeatherRecord, WeatherData

@activity.defn
async def greet(name: str) -> str:
    return f"Hello {name}"


@activity.defn
async def fetch_weather() -> dict:
    """Fetch weather data for Chiang Mai from OpenWeatherMap API and save to database."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY environment variable not set")

    # Fetch from OpenWeatherMap API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": "Chiang Mai", "appid": api_key},
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()

    # Parse weather data and convert temperature from Kelvin to Celsius
    weather_data = WeatherData(
        location="Chiang Mai",
        weather_status=data["weather"][0]["main"],
        temperature=round(data["main"]["temp"] - 273.15, 2),
        humidity=data["main"]["humidity"],
        description=data["weather"][0]["description"],
    )

    # Save to database
    with get_db_session() as session:
        record = WeatherRecord(
            location=weather_data.location,
            weather_status=weather_data.weather_status,
            temperature=weather_data.temperature,
            humidity=weather_data.humidity,
            description=weather_data.description,
        )
        session.add(record)
        session.flush()  # Get the ID without full commit

        return {
            "id": record.id,
            "location": record.location,
            "weather_status": record.weather_status,
            "temperature": record.temperature,
            "humidity": record.humidity,
            "description": record.description,
            "timestamp": record.timestamp.isoformat() if record.timestamp else None,
        }