import pytest

from services.geocoder_service import GeocoderService


@pytest.fixture
def geocoder():
    return GeocoderService()


def test_get_coordinates(geocoder):
    coordinates = geocoder.get_coordinates_by_city("Stockholm")
    print(coordinates)
    assert coordinates is not None
    assert len(coordinates) == 2
    assert coordinates[0] == float(59.3251172)  # Expected latitude
    assert coordinates[1] == float(18.0710935)  # Expected longitude


def test_get_coordinates_by_city_not_valid_city(geocoder):
    """Test for the case when city is NonExistent"""
    with pytest.raises(ValueError):
        geocoder.get_coordinates_by_city("NonExistentCity")
