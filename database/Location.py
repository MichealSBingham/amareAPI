import pytz
import timezonefinder, pytz
from geopy.geocoders import Nominatim

class Location:

    geolocator = Nominatim(user_agent="amare")

    def __init__(self, info_dict=None, city=None, geohash=None, latitude=None, longitude=None, state=None, country=None, search=None, search_address_result=None):
        self.info_dict = info_dict
        if info_dict is None:
            info_dict = {}
        self.search = search # Location searched or entered by user when lat/lon are not specified. Such as "new york city", or "atlanta, ga" or "One world trade center" . Natural language
        self.city = info_dict.get("city")
        self.geohash = info_dict.get("geohash")
        lat = info_dict.get("latitude")
        lon = info_dict.get("longitude")


        if lat is None:
            self.latitude = latitude
        else:
            self.latitude = lat
        if lon is None:
            self.longitude = longitude
        else:
            self.longitude = lon

        self.state = info_dict.get("state")
        self.country = info_dict.get("country")
        self.searched_address_result = None


    def dict(self):
        if self.info_dict is None or self.info_dict == {}:
            return {}

        return {
            "city": self.city,
            "geohash": self.geohash,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "state": self.state,
            "country": self.country,
        }

# Returns the timezone or None if could not find it given location
    def timezone(self):
        try:
            tf = timezonefinder.TimezoneFinder()
            tzString = tf.certain_timezone_at(lat=self.latitude, lng=self.longitude)
            return pytz.timezone(tzString)
        except:
            return None

# Will retreive the coordinates of location if they've been instantiated with object
    # otherwise, will try to get the coordinates from a natural language location/address string 'search', None if can't return it
    def coordinates(self):
        if self.latitude != None and self.longitude != None:
            return (self.latitude, self.longitude)
        else:
            try:
                location = self.geolocator.geocode(self.search)
                self.searched_address_result = location.address
                self.latitude = location.latitude
                self.longitude = location.longitude
                return (location.latitude, location.longitude)
            except:
                return None




        pass



