import flatlib
from flatlib import const
from flatlib.aspects import Aspect
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import aspects
from flatlib import angle
from flatlib.object import Object as Obj

"""
Example Usage of Planet Obj : 
planet = user.sun # Object from flatlib 
planet.sign // returns 'Cancer' 
planet.element() // returns 'Fire' ** Element of the planet, not the sign 
planet.signlon // returns '28.8120704...' Int representation of angle. 
planet.movement() // returns 'Direct' or 'Retrograde'
planet.isRetrograde() // returns True or False if planet is in Retrograde 
"""

#Converts Object (flatlib.object) [planet] to a dictionary. Orb decides on a cusp
def planetToDict(planet, set_orb=3):
    sign = planet.sign              #Sign (String) 'Cancer', 'Scorpio', etc
    angle = planet.signlon          #Angle (Float, [0,30) )   25.343223, 3.2
             # Speed (Float) degrees per day through the zodiac

    if planet.id != "Asc" and planet.id != "MC":
        is_retrograde = planet.isRetrograde()       # True or False in retrograde
        speed = planet.lonspeed
    else:
        is_retrograde = None                #MC and ASC cannot retrograde
        speed = None

    element = getElementFromSign(sign)    # 'Water', etc. , element of sign

    cusp_sign = isOnCuspOf(planet, set_orb)         #will return None if no cusp
    cusp_element = getElementFromSign(cusp_sign)
    if cusp_sign is not None:
        almost = {"cusp_sign": cusp_sign, "cusp_element": cusp_element}
        is_on_cusp = True
    else:
        is_on_cusp = False
        almost = None

    planet_data = {

        "sign": sign,
        "element": element,
        "angle": angle,
        "speed": speed,
        "is_retrograde": is_retrograde,
        "is_on_cusp": is_on_cusp,
        "almost": almost

    }

    cleaned_planet_data = {k: v for k, v in planet_data.items() if
                             v is not None and v != '' and (v != {}) and (v != [])}

    return cleaned_planet_data

def angleToDic(angle, set_orb=3):

    sign = angle.sign
    element = getElementFromSign(sign)
    measured_angle = angle.signlon
    cusp_sign = isOnCuspOf(angle, set_orb)
    cusp_element = getElementFromSign(cusp_sign)

    if cusp_sign is not None:
        almost = {"cusp_sign": cusp_sign, "cusp_element": cusp_element}
        is_on_cusp = True
    else:
        is_on_cusp = False
        almost = None



    angle_data  = {

        "sign": sign,
        "element": element,
        "angle": measured_angle,
        "is_on_cusp": is_on_cusp,
        "almost": almost

    }

    cleaned_angle_data = {k: v for k, v in angle_data.items() if
                           v is not None and v != '' and (v != {}) and (v != [])}
    return cleaned_angle_data


"""
// Aspects 
aspects.isAspecting(planet1, planet2, const.ALL_ASPECTS) // returns if planet1 aspects planet2 within its orb 
aspects.hasAspect(planet1, planet2, const.ALL_ASPECTS) // returns True or False 
aspects.getAspect(planet1, planet2, const.ALL_ASPECTS) // returns 'Aspect' object 

[ Aspect object ]
aspect = aspects.getAspect(planet1, planet2, const.ALL_ASPECTS)
aspect.mutualAspect() // returns if both objects are within aspect orb 
aspect.mutualMovement() // returns if both are mutually Applying or Seperating 
aspect.movement() // 'Applicative' or 'Seperating' of active planet 
aspect.getRole(planet.id) // Returns {'role': 'passive', 'inOrb': True, 'movement': 'None'} dictionary 
aspect.type // 120 , returns Int of degrees the aspect is ...> 

"""

# Utility Functions ...

#date: date Timestamp from database OR flatlib.datetime Datetime object
#birth_location : Location  (must have lattidude and longitude)
# WARNING - to be safe, please ONLY pass a flatlib.datetime Datime object here OR a timestamp
# IF YOU PASS A regular datetime like datetime.now() IT WILL NOT COMPUTE PROPER NATAL CHART
# BECAUSE when it converts it to flatlib.Datetime it will assume UTC time and not return proper date
def get_natal_chart(date, birth_location):

    lat, lon = birth_location.coordinates()
    if ( date is None ) or (birth_location is None):
        return None
    if type(date) is Datetime:  #it's already a flatlib.datetime Datetime object no need to convert it to otherwise
        date_ = date

    else: # It's a timestamp from the database
        date_ = __proper_date__(date)

    return Chart(date_, GeoPos(lat, lon), IDs=const.LIST_OBJECTS)

# converts a datetime object to the proper 'Datetime' object for the natal chart api
def __proper_date__(date):
    date_string = str(date.date()).replace('-', '/')
    time = date.time().strftime("%H:%M:%S")
    try:
        timezone = date.tzname().replace('UTC', '')
        if timezone == '':
            timezone = '+00:00'
    except:
        if date.tzname() is None:
            return Datetime(date_string, time)

    return Datetime(date_string, time, utcoffset=timezone)

# ***Returns the name of the aspect from the degrees
def aspectFromDeg(deg):
    if deg == const.NO_ASPECT:
        return 'NO ASPECT'
    elif deg == const.CONJUNCTION:
        return 'CONJUNCTION'
    elif deg == const.SEXTILE:
        return 'SEXTILE'
    elif deg == const.SQUARE:
        return 'SQUARE'
    elif deg == const.TRINE:
        return 'TRINE'
    elif deg == const.OPPOSITION:
        return 'OPPOSITION'
    elif deg == const.SEMISEXTILE:
        return 'SEMISEXTILE'
    elif deg == const.SEMIQUINTILE:
        return 'SEMIQUINTILE'
    elif deg == const.SEMISQUARE:
        return 'SEMISQUARE'
    elif deg == const.QUINTILE:
        return 'QUINTILE'
    elif deg == const.SESQUIQUINTILE:
        return 'SESQUIQUINTILE'
    elif deg == const.SESQUISQUARE:
        return 'SESQUISQUARE'
    elif deg == const.BIQUINTILE:
        return 'BIQUINTILE'
    elif deg == const.QUINCUNX:
        return 'QUINCUNX'
    else:
        return 'NO ASPECT'

def getSignAndIncludeCusp(planet, set_orb=3):
    cusp_sign = isOnCuspOf(planet, set_orb)
    if cusp_sign is None:
        return planet.sign
    else:
        return planet.sign + '(' + cusp_sign + ')'

def signWithCusp(planet, set_orb=3):
    return getSignAndIncludeCusp(planet, set_orb)

#Returns the sign this planet is on the cusp on, None if on no cusp. Default orb is 3 deg to define cusp
def isOnCuspOf(planet, set_orb=3):
    index = const.LIST_SIGNS.index(planet.sign)
    goBackwards = False
    goForwards = False
    if planet.signlon < set_orb:
        # on cusps on planet before
        goBackwards = True
    if 30 - planet.signlon < set_orb:
        goForwards = True
    if goForwards == False and goBackwards == False:
        return None
    if goForwards:
        if index == 11:
            return const.LIST_SIGNS[0]
        else:
            return const.LIST_SIGNS[index+1]
    if goBackwards:
        return const.LIST_SIGNS[index-1]

# ***Returns the element of that particular sign... returns [] if it's on cusps
def getElement(planet, set_orb=3):
    sign = planet.sign
    cusp_sign = isOnCuspOf(planet, set_orb)
    if cusp_sign is None:
        return getElementFromSign(sign)
    else:
        return getElementFromSign(sign) + '(' + getElementFromSign(cusp_sign) + ')'

def getElementFromSign(sign):
    if sign == 'Aries':
        return 'Fire'
    if sign == 'Taurus':
        return 'Earth'
    if sign == 'Gemini':
        return 'Air'
    if sign == 'Cancer':
        return 'Water'
    if sign == 'Leo':
        return 'Fire'
    if sign == 'Virgo':
        return 'Earth'
    if sign == 'Libra':
        return 'Air'
    if sign == 'Scorpio':
        return 'Water'
    if sign == 'Sagittarius':
        return 'Fire'
    if sign == 'Capricorn':
        return 'Earth'
    if sign == 'Aquarius':
        return 'Air'
    if sign == 'Pisces':
        return 'Water'

# returns the valid aspects from aspect array.. meaning will exclude all of the 'NO ASPECTS'
def validAspects_(aspects):
    valid = []
    for aspect in aspects:
        if not (aspect.type == 'NO ASPECT'):
            valid.append(aspect)
    return valid

#return example: get_aspect_of_type('SQUARE') returns all of the square aspects
def get_aspects_of_type(aspects, type):
    valid = []
    for aspect in aspects:
        if (aspect.type == type):
            valid.append(aspect)
    return valid


# Angle the sign starts at relative to Aries being at 0 degrees
# Will return float / double version of angle where the minutes and seconds are converted to de
def __angleOnCircleSignStartsAt(sign):
    signs = const.LIST_SIGNS
    return 30*signs.index(sign)

#returns the angle the planet is positioned relative to circle itself 0-360 deg
def trueAngle(planet):
    deg = planet.signlon
    return __angleOnCircleSignStartsAt(planet.sign) + deg

def angleBetween(planet1, planet2):
    a1 = trueAngle(planet1)
    a2 = trueAngle(planet2)
    return abs(a1-a2)






class DetailedAspect:

## Consider out of sign conjunctions etc
    def __init__(self,
                 first=None,            #  First planet in the aspect (Sun, Moon, ... )
                 second=None,           #  Second planet in the aspect (Mercury, Moon, ...)
                 isMutual=None,         #  if the aspect is mutual with both planets (True or False)
                 movement=None,         #  'Applicative' or 'Seperative' of active planet
                 mutualMovement=None,   #  if both planets are moving the same
                 type=None,             #  aspect type .. ('Conjunction', 'Sextile', ... etc)
                 active=None,           #  which planet is active    ('Sun', 'Moon', etc...)
                 passive=None,          #  which planet is passive .. ^
                 orb=None,              #  returns the degrees as a decimal representation (without minutes) 23.3234
                 degree=None,           # returns degrees as a string with minutes .. '23' 342''
                 elements=None,
                 isSpecial=False,       # Aspects that are a result of being on cusps and tradtionally would not occur. Example: out of sign conjunctions, Water/Fire trines, etc
                 aspectsToGet=const.ALL_ASPECTS,
                 active_planet_owner=None,
                 passive_planet_owner=None,
                 first_planet_owner=None,
                 second_planet_owner=None,
                 name = None
                 ):

        aspect = aspects.getAspect(first, second, aspectsToGet)
        self.aspect = aspect
        self.first = first
        self.second = second
        self.active = aspect.active.id
        self.passive = aspect.passive.id
        self.isMutual = aspect.mutualAspect()
        self.movement = aspect.movement()
        self.mutualMovement = aspect.mutualMovement()
        self.type = aspectFromDeg(aspect.type)
        self.orb = aspect.orb
        self.degree = angle.toString(aspect.orb)
        self.elements = [getElement(first), getElement(second)]
        self.active_planet_owner = active_planet_owner
        self.passive_planet_owner = passive_planet_owner
        self.name = (first.id, second.id)
        #isspecial

        # Returns the aspect type with the owner's of the planets ex: 'Micheal-Sun TRINE Moon-Kate'

    def angle(self):
        p1 = self.first
        p2 = self.second
        return angleBetween(p1, p2)


    def __aspectTypeString__(self):
        if self.active_planet_owner is None or self.passive_planet_owner is None:
            return ""
        return "%s-%s %s %s-%s" % ( self.active_planet_owner.name, self.active, self.type, self.passive, self.passive_planet_owner.name)

    def __str__(self):
        return "<%s %s %s %s  @ %s  // .........%s......... (%s/%s) ................ || [%s and %s] >" % (self.active, self.type, self.passive, self.degree, angle.toString(self.angle()), self.__aspectTypeString__(), getSignAndIncludeCusp(self.first), getSignAndIncludeCusp(self.second), self.elements[0], self.elements[1])

    def __hash__(self):
        return hash((self.type, self.degree, self.active, self.passive))

    def __eq__(self, other):
        sameType = (self.type == other.type)
        sameDeg  = (self.degree == other.degree)
        sameActivePlanet = (self.active == other.active)
        samePassivePlanet = (self.passive == other.passive)
        return (sameType and sameDeg and sameActivePlanet and samePassivePlanet)

    def __ne__(self, other):
        sameType = (self.type == other.type)
        sameDeg  = (self.degree == other.degree)
        sameActivePlanet = (self.active == other.active)
        samePassivePlanet = (self.passive == other.passive)
        return not (sameType and sameDeg and sameActivePlanet and samePassivePlanet)

    def __lt__(self, other):
        s = self.active + self.passive
        s2 = other.active + other.passive
        return s < s2

    def __le__(self, other):
        s = self.active + self.passive
        s2 = other.active + other.passive
        return s <= s2

    def __gt__(self, other):
        s = self.active + self.passive
        s2 = other.active + other.passive
        return s > s2

    def __ge__(self, other):
        s = self.active + self.passive
        s2 = other.active + other.passive
        return s >= s2


#// Collection of detailed aspects, between 2 persons or 2 natal charts
class Aspects:

    #Aspects are an array of aspects
    def __init__(self, aspects):
        aspects.sort()
        self.all = aspects #returns a list of 'all' of the aspects
        self.list = aspects
        self.users = self.__getUsersThatBelongToThisChart()

    def __str__(self):
        s = ""
        for aspect in self.all:
            s += "\n" + aspect.__str__()

        return s

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return (x for x in self.list)

    ## Gets a particular aspect, example: Mars/Venus aspect --> get('Mars', 'Venus')
    def get(self, planet1, planet2):
        for aspect in self.list:
            if aspect.first.id == planet1:
                if aspect.second.id == planet2:
                    return aspect

    def Get(self, planet1, planet2):

        a1 = None
        a2 = None

        for aspect in self.list:
            if aspect.first.id == planet1:
                if aspect.second.id == planet2:
                    a1 = aspect

        for aspect in self.list:
            if aspect.second.id == planet1:
                if aspect.first.id == planet2:
                    a2 = aspect

        return (a1, a2)



    # Gets the users that are in this chart, ex: If an 'Aspects' object contains aspects between Micheal and Zyla it'll return Micheal and Zyla user objects
    def __getUsersThatBelongToThisChart(self):
        users = []
        for aspect in self.list:
            users.append(aspect.active_planet_owner)
            users.append(aspect.passive_planet_owner)
        return list(set(users))

    #Returns 'Aspects' where the active planet belongs to user=user
    # Typically, the synastry chart from User's point of view (where User is the outer planet) is returned from this
    # Example: Synastry between Micheal & Gracen, Micheal is the outer planet, ---> this func returns chart.
    def where_active_planet_belongs_to(self, user):
        aspects = []
        for aspect in self.list:
            if aspect.active_planet_owner == user:
                aspects.append(aspect)
        return Aspects(aspects)

    def where_passive_planet_belongs_to(self, user):
        aspects = []
        for aspect in self.list:
            if aspect.passive_planet_owner == user:
                aspects.append(aspect)
        return Aspects(aspects)

    def valid(self):
        aspects = validAspects_(self.list)
        return Aspects(aspects)

    def squares(self):
        return Aspects(get_aspects_of_type(self.list, 'SQUARE'))

    def trines(self):
        return Aspects(get_aspects_of_type(self.list, 'TRINE'))

    def no_aspects(self):
        return Aspects(get_aspects_of_type(self.list, 'NO ASPECT'))

    def conjunctions(self):
        return Aspects(get_aspects_of_type(self.list, 'CONJUNCTION'))

    def sextiles(self):
        return Aspects(get_aspects_of_type(self.list, 'SEXTILE'))

    def oppositions(self):
        return Aspects(get_aspects_of_type(self.list, 'OPPOSITION'))

    def semisextiles(self):
        return Aspects(get_aspects_of_type(self.list, 'SEMISEXTILE'))

    def semiquintiles(self):
        return Aspects(get_aspects_of_type(self.list, 'SEMIQUINTILE'))

    def semisquares(self):
        return Aspects(get_aspects_of_type(self.list, 'SEMISQUARE'))

    def quintiles(self):
        return Aspects(get_aspects_of_type(self.list, 'QUINTILE'))

    def sesquiquintiles(self):
        return Aspects(get_aspects_of_type(self.list, 'SESQUIQUINTILE'))

    def sesquisquares(self):
        return Aspects(get_aspects_of_type(self.list, 'SESQUISQUARE'))

    def biquintiles(self):
        return Aspects(get_aspects_of_type(self.list, 'BIQUINTILE'))

    def quincunxes(self):
        return Aspects(get_aspects_of_type(self.list, 'QUINCUNX'))






























""""
#Represents a pair of users, used to run synastry and get aspects.
class Pairing:

    def __init__(self, user1, user2, aspectsToGet=const.ALL_ASPECTS):
        self.user1 = user1
        self.user2 = user2
        self.all = user1.aspects(user2, aspectsToGet=aspectsToGet)   #Gets the aspects between two users (all of them)
        self.aspects = validAspects(self.all)                  # Returns all 'real' aspects.

"""
