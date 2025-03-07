import logging

from fastapi import FastAPI, HTTPException, Depends

from models.weather import WeatherResponse
from services.geocoder_service import GeocoderService
from weather_client import WeatherClient

app = FastAPI()


async def get_geocoder():
    return GeocoderService()


async def get_weather_client():
    return WeatherClient()


@app.get("/")
async def index() -> set[str]:
    return {"landing page"}


@app.get("/weather", response_model=WeatherResponse)
async def get_city_weather(city_name: str, geocoder_service: GeocoderService = Depends(get_geocoder),
                           weather_client=Depends(get_weather_client)) -> WeatherResponse:
    try:
        # Step 1: Get the coordinates of the city
        lat, lon = geocoder_service.get_coordinates_by_city(city_name)

        # Step 2: Get the weather data for the city
        if lat is not None and lon is not None:
            temperature, description, wind_speed = weather_client.get_weather(lat, lon)

            # Step 3: Return the response in the desired format
            return WeatherResponse(
                temperature=temperature,
                weather_description=description,
                city=city_name,
                coordinates={"lat": lat, "lon": lon},
                wind_speed=wind_speed
            )
    except HTTPException as e:
        logging.exception(f"Something went wrong when trying to get weather for city {city_name}")
        raise e
