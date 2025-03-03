from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from main import app, GeocoderService, WeatherService  # Import your FastAPI app and services


@pytest.fixture
def geocoder_mock():
    """Fixture to mock GeocoderService."""
    mock = MagicMock(GeocoderService)
    mock.get_coordinates_by_city.return_value = (40.7128, -74.0060)  # Example: New York coordinates
    return mock


@pytest.fixture
def weather_service_mock():
    """Fixture to mock WeatherService."""
    mock = MagicMock(WeatherService)
    mock.get_weather.return_value = (25, "Clear sky")  # Example: temperature and description
    return mock


@pytest.fixture
def client(geocoder_mock, weather_service_mock):
    """Fixture to create a test client with mocked dependencies."""
    # Override the dependencies of the FastAPI app
    app.dependency_overrides[GeocoderService] = geocoder_mock
    app.dependency_overrides[WeatherService] = weather_service_mock

    # Return a TestClient instance for making requests
    return TestClient(app)


def test_get_city_weather(client):
    """Test for the /weather endpoint."""
    response = client.get("/weather?city_name=New%20York")

    assert response.status_code == 200
    data = response.json()

    # Check that the response contains expected values
    assert data["city"] == "New York"
    assert data["coordinates"] == {"lat": 40.7127281, "lon": -74.0060152}
    assert data["temperature"] == float(0.3)
    assert data["weather_description"] == "clearsky_day"


def test_get_city_weather_not_found(client, geocoder_mock, weather_service_mock):
    """Test for the case when city coordinates cannot be found."""
    geocoder_mock.get_coordinates_by_city.side_effect = HTTPException(status_code=404, detail="City not found")
    with pytest.raises(ValueError):
        client.get("/weather?city_name=NonExistentCity")
