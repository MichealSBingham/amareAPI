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

    def __init__(self, id=None, data=None,
                           hometown=None,
                           residence=None,
                           birthday=None,  #Only a flatlib.datetime Datetime object
                           name=None,
                          profile_image_url=None,
                           sex=None,
                           orientation=None,
                           natal_chart = None,
                           exists = False,
                           known_time=False,
                           ):

        self.id = id

        if self.id is None or self.id == '':
            self.__data = {} #if .__data is {} or None, this object wasn't read from the database
            userWasReadFromDatabase = False
            self.__was_read_from_database = userWasReadFromDatabase
        else:
            self.__data = self.users_ref.document(f'{id}').get().to_dict()
            userWasReadFromDatabase = True
            self.__was_read_from_database = userWasReadFromDatabase


        if self.__data is None or self.__data == {}:
            self.exists = False
        else:
            self.exists = True

        if userWasReadFromDatabase and self.exists:

            self.name = self.__data.get('name')
            self.profile_image_url = self.__data.get('profile_image_url')
            self.sex = self.__data.get('sex')
            self.orientation = self.__data.get('orientation')
            self.known_time = self.__data.get('known_time', False)

            location = Location(info_dict=self.__data.get('hometown', {}))
            if location.info_dict == {} or location.info_dict is None:
                self.hometown = {}
            else:
                self.hometown = Location(info_dict=self.__data.get('hometown', {}))

            residence = Location(info_dict=self.__data.get('residence'))
            if residence.info_dict == {} or residence.info_dict is None:
                self.residence = {}
            else:
                self.residence = Location(info_dict=self.__data.get('residence', {}))

            #Retreiving timestampe from database
            bdayObjectFromDatabase = self.__data.get('birthday')
            if bdayObjectFromDatabase is not None:
                self.birthday = bdayObjectFromDatabase.get('timestamp') #returns TIMESTAMP(datetime) object
            else:
                self.birthday = None  #No birthday saved.

        else: #User object was instantiated manually
            self.name = name
            self.hometown = hometown #Should be a Location object
            self.residence = residence # ^
            self.birthday = birthday # should be a flatlib.datetime Datetime object
            self.profile_image_url = profile_image_url
            self.sex = sex
            self.orientation = orientation
            self.known_time = known_time



        # Gets the natal chart based on Date
        #self.birthday should be Timestamp or flatlib.datetime.Datetime

        self.natal_chart = NatalChart.get_natal_chart(self.birthday, self.hometown)
        if self.natal_chart is None:
            self.natal_chart = {}  #could not create natal chart from info

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
        if (self.known_time == True):
            self.asc = self.natal_chart.get('Asc')
            self.mc = self.natal_chart.get('MC')
            self.ic = self.natal_chart.get('IC')
            self.desc = self.natal_chart.get('Desc')
        else:
            self.asc = None
            self.mc = None
            self.ic = None
            self.desc = None
        self.north_node = self.natal_chart.get('North Node')
        self.south_node = self.natal_chart.get('South Node')

        self.syzygy = self.natal_chart.get('Syzygy')
        self.pars_fortuna = self.natal_chart.get('Pars Fortuna')




    def dict(self):


        if self.hometown is None:
            htown = {}
            tz = None
        else:
            htown = self.hometown.dict()
            tz = self.hometown.timezone() # timezone object or None

        if self.residence is None:
            rtown = {}
        else:
            rtown = self.residence.dict()

# Converts the datetime object to a string, also changes the timezone
        if self.birthday is None:
            bday_string = None
        else:
            if self.__was_read_from_database:
                # we should have a timestamp object (datetime google apis)
                if self.known_time:
                    bday_string = self.birthday.replace(tzinfo=self.birthday.tzinfo).astimezone(
                        tz=tz).strftime("%a %d %b %Y %H:%M:%S %Z")
                else:
                    bday_string = self.birthday.strftime("%a %d %b %Y")
            else:
                bday_string = str(self.birthday)



        user_data_dict = {
            "name": self.name,
            "sex": self.sex,
           "birthday": bday_string,
            "known_time": self.known_time,
           "orientation": self.orientation,
           "profile_image_url": self.profile_image_url,
           "hometown": htown,
           "residence": rtown
        }
        cleaned_user_data_dic = {k: v for k, v in user_data_dict.items() if v is not None and v != '' and (v != {}) and  (v != [])}


        return cleaned_user_data_dic

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (self.id == other.id)

    #returns all of the planets used for synastry.. will include MC and ASC even though they are not planets
    def planets(self):
        ps = [self.sun, self.moon, self.mercury, self.venus, self.mars, self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto, self.north_node, self.south_node, self.chiron]
        return [p for p in ps if p ] # removes all 'None'

    def angles(self):
        if not self.known_time:
            return [] #cannot compute angles without known birth_time
        else:
            return [self.ic, self.mc, self.desc, self.asc]

#returns everything we use for synastry to get aspects, gets the planets and angles currently
    def __all_for_synastry(self):
        return self.planets() + self.angles()

    #returns all aspects between each planet , even if there is 'NO ASPECT' between them
    # returns [DetailedAspect]
    def __get_aspects(self, user2=None, aspectsToGet=const.ALL_ASPECTS):
        aspects = []
        if user2 is None:
            #aspects = []
            planets = self.__all_for_synastry()
            for pair in itertools.combinations(planets, 2):
                try:
                    aspect = NatalChart.DetailedAspect(pair[0], pair[1], aspectsToGet=aspectsToGet)
                    aspects.append(aspect)
                except:
                    print("Failed to get aspect between " + pair[0].id + " and " + pair[1].id)
                    pass
        if not (user2 is None):
            for user1planet in self.__all_for_synastry():
                for user2planet in user2.__all_for_synastry():
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

    # Return the natal chart as a dictionary
    def natal(self, set_orb=3):
        from astrology.NatalChart import planetToDict, angleToDic

        name = self.name
        sex = self.sex
        birth_place = self.hometown.dict()

        if self.__was_read_from_database:
            # we should have a timestamp object (datetime google apis)
            tz = self.hometown.timezone()
            if self.known_time:
                bday_string = self.birthday.replace(tzinfo=self.birthday.tzinfo).astimezone(
                tz=tz).strftime("%a %d %b %Y %H:%M:%S %Z")
            else:
                bday_string = self.birthday.strftime("%a %d %b %Y")

        else:
            bday_string = str(self.birthday)


        natal_dic = {}

        planets = self.planets()
        planetsDic = {}
        for planet in planets:
            planetsDic[planet.id] = planetToDict(planet, set_orb=set_orb)


        angles = self.angles()
        anglesDic = {}
        if angles != None:
            for angle in angles:
                anglesDic[angle.id] = angleToDic(angle, set_orb=set_orb)




        natal_dic["houses"] = "UNDER CONSTRUCTION"
        natal_dic["aspects"] = "UNDER CONSTRUCTION"
        natal_dic["name"] = name
        natal_dic["birthday"] = bday_string
        natal_dic["birth_place"] = birth_place
        natal_dic["planets"] = planetsDic
        natal_dic["angles"] = anglesDic


        cleaned_natal_data = {k: v for k, v in natal_dic.items() if
                              v is not None and v != '' and (v != {}) and (v != [])}

        return cleaned_natal_data



















