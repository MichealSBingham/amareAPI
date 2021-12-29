import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud import firestore
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
    generated_users_ref = db.collection(f'generated_users')

    def __init__(self, id=None, data=None,
                           hometown=None,
                           residence=None,
                           birthday=None,  #Only a flatlib.datetime Datetime object
                           name=None,
                           username=None,
                          profile_image_url=None,
                           sex=None,
                           orientation=None,
                           natal_chart = None,
                           exists = False,
                           known_time=False,
                        do_not_fetch=False # If true, data will not be fetched from database even if you provide ID (to prevent a read)
                           ):

        self.id = id

        if self.id is None or self.id == '' or do_not_fetch == True:
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
            self.username = self.__data.get('username')
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
            self.username = username



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


        # Get the houses 
        self.house1 = self.natal_chart.get('House1')
        self.house2 = self.natal_chart.get('House2')
        self.house3 = self.natal_chart.get('House3')
        self.house4 = self.natal_chart.get('House4')

        self.house5 = self.natal_chart.get('House5')
        self.house6 = self.natal_chart.get('House6')
        self.house7 = self.natal_chart.get('House7')
        self.house8 = self.natal_chart.get('House8')

        self.house9 = self.natal_chart.get('House9')
        self.house10 = self.natal_chart.get('House10')
        self.house11 = self.natal_chart.get('House11')
        self.house12 = self.natal_chart.get('House12')



    @classmethod
    def random_new_user(cls):
        """Creates new user randomly and sets in database """
        rand = User.random()
        rand.new()

    @classmethod
    def random(cls):
        """ Creates a random user object without setting in database"""
        from faker import Faker
        from database.Location import Location
        import random
        from randomuser import RandomUser
        from random_username.generate import generate_username

        fake = Faker()
        fake.seed_locale('en_US', 0)

        random_hometown = Location().random()
        random_residence = Location().random()
        random_date = fake.date_time_between(start_date='-30y', end_date='now')
        knows_birthtime = bool(random.getrandbits(1))
        random_username = generate_username()[0]

        # Random User Data
        random_gender = random.choice(['female', 'male', 'transfemale', 'transmale', 'non_binary'])
        if random_gender == 'male' or random_gender == 'female':
            user = RandomUser({'gender': random_gender})
        elif random_gender == 'transfemale':
            user = RandomUser({'gender': 'female'})
        elif random_gender == 'transmale':
            user = RandomUser({'gender': 'male'})
        else:
            user = RandomUser()

        random_name = user.get_full_name()

        ## Generating orientation randomly, from male POV
        genders = ['male', 'female', 'non_binary', 'transmale', 'transfemale']
        randNum = random.randrange(1,5)  # can be 1 to 6
        random_orientation = []
        for _ in range(randNum):
            random_orientation.append(random.choice(genders))
        random_orientation = list(set(random_orientation))




        random_profile_pic = user.get_picture()

        return cls(do_not_fetch=True,
                   id=user.get_login_uuid(),
                   hometown=random_hometown,
                   residence=random_residence,
                   birthday=random_date,
                   known_time=knows_birthtime,
                   orientation=random_orientation,
                   profile_image_url=random_profile_pic,
                   sex=random_gender,
                   name=random_name)


    def new(self):
        """Sets the newly created user object in the database """
        newuserdic = {

            "birthday": { "day": self.birthday.day, "month": "TODO:/RandomDataMonthBorn", "year": self.birthday.year, "timestamp": self.birthday},
            "hometown": self.hometown.dict(),
            "residence": self.residence.dict(),
            "images": [], #TODO: random data for images
            "known_time": self.known_time,
            "name": self.name,
            "orientation": self.orientation,
            "profile_image_url": self.profile_image_url,
            "sex": self.sex,
            "username": self.username

        }
        self.generated_users_ref.document(self.id).set(newuserdic)
        self.set_natal_chart(real_user=False) #TODO: this should automatically happen whenever a new user is created but it's because the cloud function only detect when birthday data is changed, not created



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


    def planets(self):
        ps = [self.sun, self.moon, self.mercury, self.venus, self.mars, self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto, self.north_node, self.south_node, self.chiron]
        return [p for p in ps if p ] # removes all 'None'

    def angles(self):
        if not self.known_time:
            return [] #cannot compute angles without known birth_time
        else:
            return [self.ic, self.mc, self.desc, self.asc]

    def houses(self): 
        if not self.known_time: 
            return []
        else: 
            return [self.house1, self.house2, self.house3, self.house4, 
                    self.house5, self.house6, self.house7, self.house8, 
                    self.house9, self.house10, self.house11, self.house12]

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
        for p1 in self.__all_for_synastry():
            for p2 in user2.__all_for_synastry():
                try:
                    asp = NatalChart.DetailedAspect(p1, p2, first_planet_owner=self, second_planet_owner=user2)
                    syn.append(asp)
                except:
                    print("Failed to get aspect between " + p1.id + " and" + p2.id)
        return Aspects(syn)

    # Return the natal chart as a dictionary, will create the natal chart and set it in database
    def natal(self, set_orb=3):
        from astrology.NatalChart import planetToDict, angleToDic, aspectToDict, houseToDict

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
    # {"sun" : { planet info } #

        angles = self.angles()
        anglesDic = {}
        if angles != None:
            for angle in angles:
                anglesDic[angle.id] = angleToDic(angle, set_orb=set_orb)


        if self.known_time:
            houses = self.houses()
            housesDic = {}
            for house in houses: 
                housesDic[int( house.id.replace('House', '') )] = houseToDict(house, planets+angles )

            natal_dic['houses'] = housesDic
        else: 
            natal_dic['houses'] = None



        
        
        # Get the aspects
        aspects = self.aspects()
        aspectDic = {}
        if aspects != None:
            for aspect in aspects:
                    id = f"{aspect.name[0]} {aspect.name[1]}"
                    aspectDic[id] = aspectToDict(aspect)
                    
                    
        natal_dic["aspects"] = aspectDic
        
        natal_dic["name"] = name
        natal_dic["birthday"] = bday_string
        natal_dic["birth_place"] = birth_place
        natal_dic["planets"] = planetsDic
        natal_dic["angles"] = anglesDic
        natal_dic["part_of_fortune"] = angleToDic(self.pars_fortuna)


        cleaned_natal_data = {k: v for k, v in natal_dic.items() if
                              v is not None and v != '' and (v != {}) and (v != [])}

        return cleaned_natal_data


    def set_natal_chart(self, set_orb=3, real_user=True):
        """
    Writes the user's (self) natal chart to the database.
        :param set_orb: The orb to use when determining cusps and aspects, by default 3 degrees. Do not change without approval.
        :return: Void
        """
        def toArray(dictOfObjects):
            array = []
            for obj_name in dictOfObjects:
                this_object = dictOfObjects[obj_name]
                this_object['name'] = obj_name
                array.append(this_object)
            return array



        natal_chart_dict = self.natal(set_orb=set_orb)

        all_planets = toArray(natal_chart_dict['planets'])
        natal_chart_dict['planets'] = all_planets


        all_aspects = toArray(natal_chart_dict['aspects'])
        natal_chart_dict['aspects'] = all_aspects

        if self.known_time:
            all_angles = toArray(natal_chart_dict['angles'])
            natal_chart_dict['angles'] = all_angles

            all_houses = toArray(natal_chart_dict['houses']) 
            natal_chart_dict['houses'] = all_houses
        else:
            natal_chart_dict['angles'] = []
            natal_chart_dict['houses'] = []

        if real_user:
            self.users_ref.document(self.id).collection('public').document('natal_chart').set(natal_chart_dict, merge=True)
        else:
            self.generated_users_ref.document(self.id).collection('public').document('natal_chart').set(natal_chart_dict, merge=True)


    def balanceOfElements(self):
        """
        Returns the distribution of elements of the particular natal chart of
        :return: A dictionary with information eg {'Water': {'points': 7.0, 'percentage': 0.5384615384615384, 'isDominant': True, 'isOverlyDominant': True}, 'Earth': {'points': 5.0, 'percentage': 0.38461538461538464, 'isDominant': True, 'isOverlyDominant': False}, 'Fire': {'points': 1.0, 'percentage': 0.07692307692307693, 'isDominant': False, 'isOverlyDominant': False}, 'Air': {'points': 0.0, 'percentage': 0.0, 'isDominant': False, 'isOverlyDominant': False}}

        """
        from astrology.NatalChart import getElementFromSign, isOnCuspOf
        from astrology.Rulers import Rulers

        balance = {"Water": 0.0, "Earth": 0.0, "Fire": 0.0, "Air": 0.0}

        bodies = self.planets() + self.angles()


        for body in bodies:

            pointsForSign = 0.0
            pointsForCusp = 0.0
            # Check Sun/Moon Element
            element = getElementFromSign(body.sign)
            cusp_sign = isOnCuspOf(body, 1)

            if cusp_sign == None:
                # No cusp element so proceed normally
                if body.id == 'Sun' or body.id == 'Moon':
                    pointsForSign = 2
                
                elif body.id in ['Asc', 'MC', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
                    pointsForSign = 1

                balance[element] += pointsForSign
            else:
                # Split the point between it and the cusp element
                cusp_element = getElementFromSign(cusp_sign)
                if body.id == 'Sun' or body.id == 'Moon':
                    pointsForCusp = 1

                elif body.id in ['Asc', 'MC', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
                    pointsForCusp = 0.5

                balance[element] += pointsForCusp*2
                balance[cusp_element] += pointsForCusp * 2



        asc_rules = Rulers.ruler_of(self.asc.sign)  # ruler of the ascendant (planet)
        elem = getElementFromSign(self.natal_chart.get(asc_rules).sign)
        balance[elem] += 1

        sun_rules = Rulers.ruler_of(self.sun.sign)  # ruler of the sun
        elem = getElementFromSign(self.natal_chart.get(sun_rules).sign)
        balance[elem] += 1

        summary = {
            "Water": {
                "points": balance["Water"],
                "percentage": balance["Water"] / 13.0 ,
                "isDominant": (balance["Water"] >= 5),
                "isOverlyDominant": (balance["Water"] >= 6),
                "isWeak": (balance["Water"] <= 2)
            },

            "Earth": {
                "points": balance["Earth"],
                "percentage": balance["Earth"] / 13.0,
                "isDominant": (balance["Earth"] >= 5),
                "isOverlyDominant": (balance["Earth"] >= 6),
                "isWeak": (balance["Earth"] <= 2)
            },

            "Fire": {
                "points": balance["Fire"],
                "percentage": balance["Fire"] / 13.0,
                "isDominant": (balance["Fire"] >= 5),
                "isOverlyDominant": (balance["Fire"] >= 6),
                "isWeak": (balance["Fire"] <= 2),
            },

            "Air": {
                "points": balance["Air"],
                "percentage": balance["Air"] / 13.0,
                "isDominant": (balance["Air"] >= 5),
                "isOverlyDominant": (balance["Air"] >= 6),
                "isWeak": (balance["Air"] <= 2)
            }
        }

        return summary


    def hasDominant(self, element: str) -> bool:
        """
        Returns whether the element given is dominant in the user's natal chart
        :rtype: bool
        :param element: 'Water', 'Earth', 'Fire', or 'Air'
        :return: If the element is dominant
        """
        balanceOfElements = self.balanceOfElements()
        return balanceOfElements[element]["isDominant"]

    def hasWeak(self, element: str) -> bool:
        """
        Returns whether the element given is weak in the user's natal chart
        :rtype: bool
        :param element: 'Water', 'Earth', 'Fire', or 'Air'
        :return: If the element is weak
        """
        balanceOfElements = self.balanceOfElements()
        return balanceOfElements[element]["isWeak"]












"""

natal["angles"] = [angle]

natal chart dictionary should 
(map) natal_chart : {             n
    
          (array)  "angles" : [
                    
                    { ... // map ...} , 
                    { ... / map ... } 
          ], 
          
          ... 
    


}


"""














