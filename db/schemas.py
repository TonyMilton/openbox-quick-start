from pydantic import BaseModel, ConfigDict
from datetime import datetime


class WeatherData(BaseModel):
    """Pydantic model for weather data validation."""

    model_config = ConfigDict(from_attributes=True)

    location: str
    weather_status: str
    temperature: float
    humidity: int
    description: str
    timestamp: datetime | None = None
    id: int | None = None
