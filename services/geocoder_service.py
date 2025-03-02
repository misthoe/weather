from typing import Optional, Tuple

from geopy.geocoders import Nominatim

from settings import GEOPY_USER_AGENT


class GeocoderService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent=GEOPY_USER_AGENT)

    def get_coordinates_by_city(self, city: str) -> Optional[Tuple[float, float]]:
        location = self.geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
        else:
            raise ValueError("Not a valid city")
