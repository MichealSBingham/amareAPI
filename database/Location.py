
class Location:
    def __init__(self, info_dict=None, city=None, geohash=None, latitude=None, longitude=None, state=None, country=None):
        self.info_dict = info_dict
        if info_dict is None:
            info_dict = {}
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
