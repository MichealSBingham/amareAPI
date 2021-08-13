class Location:
    def __init__(self, info_dict, city=None, geohash=None, latitude=None, longitude=None, state=None, country=None):
        self.__info_dict = info_dict
        self.city = info_dict["city"]
        self.geohash = info_dict["geohash"]
        self.latitude = info_dict["latitude"]
        self.longitude = info_dict["longitude"]
        self.state = info_dict["state"]
        self.country = info_dict["country"]
        self.city = info_dict["city"]
