import httpx
import requests

from fastapi import HTTPException

from settings import API_URL


class WeatherService:


    @staticmethod
    def get_weather(lat: float, lon: float):

        headers = {"User-Agent": "weather_app/1.0"}
        params = {"lat": lat, "lon": lon}

        response = requests.get(API_URL, params=params, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching weather data.")

        weather_data = response.json()

        try:
            current_weather = weather_data['properties']['timeseries'][0]['data']['instant']['details']
            temperature = current_weather['air_temperature']
            description = weather_data['properties']['timeseries'][0]['data']['next_1_hours']['summary']['symbol_code']
        except KeyError:
            raise HTTPException(status_code=500, detail="Error parsing weather data.")

        return temperature, description
