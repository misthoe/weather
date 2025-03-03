from unittest.mock import patch, Mock

import pytest
from fastapi.exceptions import HTTPException

from services.weather_service import WeatherService


# Test case for successful weather data retrieval
@patch('requests.get')
def test_get_weather_success(mock_get):
    # Mock the response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "properties": {
            "timeseries": [
                {
                    "data": {
                        "instant": {
                            "details": {
                                "air_temperature": 23.5
                            }
                        },
                        "next_1_hours": {
                            "summary": {
                                "symbol_code": "clear"
                            }
                        }
                    }
                }
            ]
        }
    }

    # Set the mock response to be returned when requests.get is called
    mock_get.return_value = mock_response

    # Testing the method
    lat = 51.5074
    lon = -0.1278
    temperature, description = WeatherService.get_weather(lat, lon)

    # Assertions
    assert temperature == float(23.5)
    assert description == "clear"
    mock_get.assert_called_once_with(
        "https://api.met.no/weatherapi/locationforecast/2.0/compact",  # Replace with actual API URL
        params={"lat": lat, "lon": lon},
        headers={"User-Agent": "weather_app/1.0"}
    )


# Test case for API failure (non-200 status code)
@patch('requests.get')
def test_get_weather_api_error(mock_get):
    # Simulate an API error with a non-200 status code
    mock_response = Mock()
    mock_response.status_code = 500  # Internal Server Error
    mock_get.return_value = mock_response

    # Test if HTTPException is raised when the API status code is not 200
    with pytest.raises(HTTPException):
        WeatherService.get_weather(51.5074, -0.1278)


# Test case for missing required fields in response
@patch('requests.get')
def test_get_weather_invalid_data(mock_get):
    # Mock response with missing 'instant' and 'next_1_hours'
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "properties": {
            "timeseries": [
                {
                    "data": {}  # Missing both 'instant' and 'next_1_hours'
                }
            ]
        }
    }

    # Set the mock response
    mock_get.return_value = mock_response

    # Test if HTTPException is raised when essential data is missing in the response
    with pytest.raises(HTTPException):
        WeatherService.get_weather(51.5074, -0.1278)
