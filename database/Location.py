
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
        self.city = info_dict.get("city")
