
class Location:
    def __init__(self, info_dict, city=None, geohash=None, latitude=None, longitude=None, state=None, country=None):
        self.__info_dict = info_dict
        if info_dict is None:
            info_dict = {}
        self.city = info_dict.get("city")
        self.geohash = info_dict.get("geohash")
        self.latitude = info_dict.get("latitude")
        self.longitude = info_dict.get("longitude")
        self.state = info_dict.get("state")
        self.country = info_dict.get("country")


    def dict(self):
        if self.__info_dict is None or self.__info_dict == {}:
            return {}

        return {
            "city": self.city,
            "geohash": self.geohash,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "state": self.state,
            "country": self.country,
        }
