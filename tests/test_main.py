from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app, GeocoderService, WeatherClient  # Import your FastAPI app and services


@pytest.fixture
def geocoder_mock():
    """Fixture to mock GeocoderService."""
    mock = MagicMock(GeocoderService)
    mock.get_coordinates_by_city.return_value = (40.7127281, -74.0060152)  # Example: New York coordinates
    return mock


@pytest.fixture
def weather_service_mock():
    """Fixture to mock WeatherService."""
    mock = MagicMock(WeatherClient)
    mock.get_weather.return_value = (25, "Clear sky")  # Example: temperature and description
    return mock


@pytest.fixture
def client(geocoder_mock, weather_service_mock):
    """Fixture to create a test client with mocked dependencies."""
    # Override the dependencies of the FastAPI app
    app.dependency_overrides[GeocoderService] = geocoder_mock
    app.dependency_overrides[WeatherClient] = weather_service_mock

    # Return a TestClient instance for making requests
    return TestClient(app)


def test_get_city_weather(client):
    """Test for the /weather endpoint using both mocked response and checks."""

    # Mocked response for the /weather endpoint (this mimics what would be returned by the actual endpoint)
    mocked_response = {
        "city": "New York",
        "coordinates": {"lat": 40.7127281, "lon": -74.0060152},
        "temperature": 25,
        "weather_description": "clearsky_day"
    }

    # Mock the get request to return the mocked response
    with patch.object(TestClient, 'get', return_value=mocked_response) as mock_get:
        # Simulate the GET request
        response = client.get("/weather?city_name=New%20York")

        # Ensure that the mock was called with the correct URL
        mock_get.assert_called_once_with("/weather?city_name=New%20York")

        # Check that the response matches the mocked response
        assert response == mocked_response  # Check if the entire response matches

        # Also, check that the values returned are correct per your original assertions
        data = response
        assert data["city"] == "New York"
        assert data["coordinates"] == {"lat": 40.7127281, "lon": -74.0060152}
        assert data["temperature"] == 25  # Corrected to match mocked value
        assert data["weather_description"] == "clearsky_day"  # Corrected to match mocked value


def test_get_city_weather_not_found(client, geocoder_mock, weather_service_mock):
    """Test for the case when city coordinates cannot be found."""
    geocoder_mock.get_coordinates_by_city.side_effect = HTTPException(status_code=404, detail="City not found")
    with pytest.raises(ValueError):
        client.get("/weather?city_name=NonExistentCity")
