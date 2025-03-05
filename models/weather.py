from typing import Dict

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    weather_description: str
    coordinates: Dict[str, float]
    wind_speed: float

