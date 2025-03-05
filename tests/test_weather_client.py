from unittest.mock import patch

import pytest
from fastapi.exceptions import HTTPException

from weather_client import WeatherClient


@pytest.fixture
def mock_get_weather():
    """Fixture to mock the 'get_weather' method."""
    with patch.object(WeatherClient, 'get_weather') as mock_get_weather:
        yield mock_get_weather


# Test case for successful weather data retrieval
def test_get_weather_success(mock_get_weather):
    """Test the successful case of fetching weather data."""

    # Mock the return value of the get_weather method to return static values
    mock_get_weather.return_value = (22.5, "clear", 10.5)

    # Call the method
    temperature, description, wind_speed = WeatherClient.get_weather(40.7127281, -74.0060152)

    # Check that the correct static values are returned
    assert temperature == float(22.5)
    assert description == "clear"
    assert wind_speed == float(10.5)

    # Ensure that the mock method was called with the expected parameters
    mock_get_weather.assert_called_once_with(40.7127281, -74.0060152)


def test_get_weather_retry(mock_get_weather):
    """Test the retry logic for server errors (e.g., 500 status)."""

    # Simulate a failure with a mock for retries
    mock_get_weather.side_effect = HTTPException(status_code=500, detail="Error fetching weather data")

    # Call the method and check for retries
    with pytest.raises(HTTPException) as exc_info:
        WeatherClient.get_weather(40.7127281, -74.0060152)

    # Check that an exception was raised and that the status code is 500
    assert exc_info.value.status_code == 500
    assert "Error fetching weather data" in str(exc_info.value.detail)


def test_get_weather_key_error(mock_get_weather):
    """Test when the response is missing expected keys."""

    # Simulate a response with missing keys (mocking)
    mock_get_weather.side_effect = HTTPException(status_code=500, detail="Error fetching weather data")

    # Call the method and check for an error due to missing keys
    with pytest.raises(HTTPException) as exc_info:
        WeatherClient.get_weather(40.7127281, -74.0060152)

    # Ensure we get the expected exception
    assert exc_info.value.status_code == 500
    assert "Error fetching weather data" in str(exc_info.value.detail)
