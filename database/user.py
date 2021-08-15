import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from database.Location import Location
from astrology import NatalChart
from flatlib import const
import itertools
from astrology.NatalChart import Aspects


#Constants
PATH_TO_FIR_CREDENTIALS = 'database/amare-firebase.json'
cred = credentials.Certificate(PATH_TO_FIR_CREDENTIALS)
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


class User:

    users_ref = db.collection(f'users')

    def __init__(self, id, data=None,
                           hometown=None,
                           birthday=None,
                           name=None,
                           sex=None,
                           orientation=None,
                           natal_chart = None):
        self.id = id
        data = self.users_ref.document(f'{id}').get().to_dict()
        self.__data = data
        self.name = data['name']
        self.hometown = Location(info_dict=data['hometown'])
        self.birthday = data["birthday"]["timestamp"] # returns a Datetime object
        self.sex = data['sex']
        self.orientation = data['orientation']
        self.natal_chart = NatalChart.get_natal_chart(self.birthday, self.hometown)

        self.sun = self.natal_chart.get('Sun')
        self.moon = self.natal_chart.get('Moon')
        self.mercury = self.natal_chart.get('Mercury')
        self.venus = self.natal_chart.get('Venus')
        self.mars = self.natal_chart.get('Mars')
        self.jupiter = self.natal_chart.get('Jupiter')
        self.saturn = self.natal_chart.get('Saturn')
        self.uranus = self.natal_chart.get('Uranus')
        self.neptune = self.natal_chart.get('Neptune')
        self.pluto = self.natal_chart.get('Pluto')
        self.chiron = self.natal_chart.get('Chiron')
        self.asc = self.natal_chart.get('Asc')
        self.mc = self.natal_chart.get('MC')
        self.north_node = self.natal_chart.get('North Node')
        self.south_node = self.natal_chart.get('South Node')


    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (self.id == other.id)

    #returns all of the planets
    def planets(self):
        return [self.sun, self.moon, self.mercury, self.venus, self.mars, self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto, self.north_node, self.chiron, self.asc, self.mc]

    #returns all aspects between each planet , even if there is 'NO ASPECT' between them
    # returns [DetailedAspect]
    def __get_aspects(self, user2=None, aspectsToGet=const.ALL_ASPECTS):
        aspects = []
        if user2 is None:
            #aspects = []
            planets = self.planets()
            for pair in itertools.combinations(planets, 2):
                try:
                    aspect = NatalChart.DetailedAspect(pair[0], pair[1], aspectsToGet=aspectsToGet)
                    aspects.append(aspect)
                except:
                    print("Failed to get aspect between " + pair[0].id + " and " + pair[1].id)
                    pass
        if not (user2 is None):
            for user1planet in self.planets():
                for user2planet in user2.planets():
                    try:
                        aspect = NatalChart.DetailedAspect(user1planet, user2planet, aspectsToGet=aspectsToGet)


 ########################################################################################################
                        ##This is to determine which user has the planet responsible for the aspect ( who has the active planet in their chart)
                        # Gets planet object for the active planet

                        first = user1planet
                        if first.id == aspect.active:
                            aspect.active_planet_owner = self
                            aspect.passive_planet_owner = user2
                        else:
                            #activePlanet = user2planet
                            aspect.active_planet_owner = user2
                            aspect.passive_planet_owner = self
#################################################################################################################
                        aspects.append(aspect)
                    except:
                        print("Failed to get aspect between " + user1planet.id + " and " + user2planet.id)
                        pass
        return aspects

    #Returns an 'Aspects' object, for both users (both ways, if user1 is outter and inner on chart)
    def aspects(self, user2=None,aspectsToGet=const.ALL_ASPECTS ):
        aspects =self.__get_aspects(user2)
        return Aspects(aspects)

    #  Returns the synastry aspects between `Self` and User 2. Self will be the user/partner on the outer part of the synastry chart. This returns all aspects, between each planet between each other
    def synastry(self, user2, aspectsToGet=const.ALL_ASPECTS):
        syn = []
        for p1 in self.planets():
            for p2 in user2.planets():
                try:
                    asp = NatalChart.DetailedAspect(p1, p2, first_planet_owner=self, second_planet_owner=user2)
                    syn.append(asp)
                except:
                    print("Failed to get aspect between " + p1.id + " and" + p2.id)
        return Aspects(syn)

"""
    #Returns the synastry aspects between `Self` and User 2 where `Self` is the inner planet in synastry
    def synastry(self, user2=None,aspectsToGet=const.ALL_ASPECTS ):
        aspects =self.__get_aspects(user2)
        aspects = Aspects(aspects)
        return aspects.where_active_planet_belongs_to(self)
    
    """





















