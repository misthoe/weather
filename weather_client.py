import requests
from fastapi import HTTPException
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from settings import API_URL


class WeatherClient:
    # To handle retries for requests
    request_session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    # Attach the retry policy to the session
    adapter = HTTPAdapter(max_retries=retries)
    request_session.mount("https://", adapter)
    request_session.mount("http://", adapter)

    @staticmethod
    def get_weather(lat: float, lon: float, session=request_session):
        params = {"lat": lat, "lon": lon}

        response = session.get(API_URL, params=params, headers={"User-Agent": "weather_app/1.0"})

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Error fetching weather data, "
                                       f"here is some info of what might have gone wrong:{response.text}")

        weather_data = response.json()

        try:
            current_weather = weather_data['properties']['timeseries'][0]['data']['instant']['details']
            temperature = current_weather['air_temperature']
            wind_speed = current_weather['wind_speed']
            description = weather_data['properties']['timeseries'][0]['data']['next_1_hours']['summary']['symbol_code']
        except HTTPException:
            raise HTTPException(status_code=404, detail=f"Error fetching weather data, "
                                                        f"here is some info of what might"
                                                        f" have gone wrong:{response.text}")

        return temperature, description, wind_speed
