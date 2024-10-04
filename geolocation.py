from geopy.geocoders import Nominatim

def get_location_from_coords(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((lat, lon), language="en")
    return location.address