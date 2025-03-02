from fastapi import FastAPI, HTTPException, Depends

from services.geocoder_service import GeocoderService
from services.weather_service import WeatherService

from models.weather import WeatherResponse

app = FastAPI()


async def get_geocoder():
    return GeocoderService()


async def get_weather_service():
    return WeatherService()


@app.get("/weather", response_model=WeatherResponse)
async def get_city_weather(city_name: str, geocoder_service: GeocoderService = Depends(get_geocoder),
                           weather_service=Depends(get_weather_service)):
    try:
        # Step 1: Get the coordinates of the city
        lat, lon = geocoder_service.get_coordinates_by_city(city_name)

        # Step 2: Get the weather data for the city
        temperature, description = weather_service.get_weather(lat, lon)

        # Step 3: Return the response in the desired format
        return WeatherResponse(
            temperature=temperature,
            weather_description=description,
            city=city_name,
            coordinates={"lat": lat, "lon": lon}
        )
    except HTTPException as e:
        raise e
