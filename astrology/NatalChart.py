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

### ******************************* Utility Functions for building a Natal Chart Dict for API response *******************************

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


    try:
        house = planet.house
    except:
        house = None

    planet_data = {

        "sign": sign,
        "element": element,
        "angle": angle,
        "speed": speed,
        "is_retrograde": is_retrograde,
        "is_on_cusp": is_on_cusp,
        "almost": almost,
        "house": house

    }

    cleaned_planet_data = {k: v for k, v in planet_data.items() if
                             v is not None and v != '' and (v != {}) and (v != [])}

    return cleaned_planet_data
""""
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

    try:
        house = angle.house
    except:
        house = None


    angle_data  = {

        "sign": sign,
        "element": element,
        "angle": measured_angle,
        "is_on_cusp": is_on_cusp,
        "almost": almost,
        "house": house

    }

    cleaned_angle_data = {k: v for k, v in angle_data.items() if
                           v is not None and v != '' and (v != {}) and (v != [])}
    return cleaned_angle_data

def aspectToDict(detailed_aspect):
    a = detailed_aspect
    
    
    info = { 
        "type": a.type, #TRINE, etc
        "isMutual": a.isMutual,  # Bool
        "mutualMovement": a.mutualMovement, # Bool
        "orb":  a.orb,  # Double, degress as double
        "first": a.first.id, #first planet
        "second": a.second.id,
        "interpretation": a.interpretation()}
    
    
    cleaned_info = {k: v for k, v in info.items() if v is not None and v != '' and (v != {}) and (v != [])}

    
    return cleaned_info

#Bodies --> planet or angle 
def houseToDict(house, bodies):
    sign = house.sign # Sign the house begins in 
    angle = house.signlon  #Float value of angle it is in the sign ex: Virgo 22.45543
    size = house.size # Size of the house in degrees 
    condition = house.condition()
    #gender = house.gender()
    ruling_bodies = []
    for body in bodies: 
        if house.hasObject(body):
            ruling_bodies.append(body.id)

    house_data = {

        "sign": sign, 
        "angle": angle, 
        "size": size, 
        "condition": condition, 
      #  "gender": gender,  causes an error in 9th house for me at least, mine is in libra
        "contains": ruling_bodies

    }

    cleaned_house_data = {k: v for k, v in house_data.items() if
                             v is not None and v != '' and (v != {}) and (v != [])}

    return cleaned_house_data






## ******************************* End of Utility Functions  *******************************

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
    import swisseph as swe
    import os
    # Have to add proper file to proper path so that it can read the astrology data
    path = os.path.dirname(flatlib.__file__)
    new_path = os.path.join(path, 'resources', 'swefiles')
    swe.set_ephe_path(new_path)

    #print("Getting natal chart for date: " + str(date))
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
    # {date_string} and time {time}')
    
    try:
        timezone = date.tzname().replace('UTC', '')
        #print(f'The timezone {timezone}')
        if timezone == '':
            timezone = '+00:00'
    except:
        if date.tzname() is None:
            #print('no timezone assuming UTC time')
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
    """
    Returns the Element of a particular sign
    :param sign: The sign of the element. E.g. 'Cancer', 'Scorpio'
    :type sign: str
    :return: Element of the sign. 'Fire', 'Air', 'Earth', or 'Water'
    :rtype: str
    """
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





#*** Given planet, returns the aspects each sign in each degree makes with it 
# Returns [ [sign, degree, aspect], [sign, degree, aspect] ]   
# 
def allPossibleAspectsEachSignMakesWith(planet1): 

    allDegreesForPlanet = [] # const.LIST_PLANETS


    # Will return something like 
    #( Cancer, 2 , 'SQUARE' ) or 
    # [ ( Planet, DetailedAspect) ] 
    pass 


class DetailedAspect:

    harmonious_aspects = [ aspectFromDeg(const.TRINE),
                           aspectFromDeg(const.CONJUNCTION),
                           aspectFromDeg(const.SEXTILE),
                           aspectFromDeg(const.SEMIQUINTILE),
                           aspectFromDeg(const.QUINTILE),
                           aspectFromDeg(const.SESQUIQUINTILE),
                           aspectFromDeg(const.BIQUINTILE)

                            ]

                            
    disharmonious_aspects = [ aspectFromDeg(const.SQUARE), aspectFromDeg(const.SEMISQUARE), aspectFromDeg(const.SESQUISQUARE), aspectFromDeg(const.OPPOSITION), aspectFromDeg(const.QUINCUNX) ]


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
                 name=None, 
                 harmonyScoreAssigned=None #this is only adjusted if this aspect is from an algorithm that assigns harmony scores
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
        self.first_planet_owner = first_planet_owner
        self.second_planet_owner = second_planet_owner
        self.name = (first.id, second.id)
        self.harmonyScoreAssigned = harmonyScoreAssigned
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

        from colorama import Fore
        from colorama import Style

        desc = self.interpretation()

        if self.isHarmonious():
            color = Fore.GREEN
        elif self.isChallenging():
            color = Fore.RED
        else:
            color = Fore.WHITE



        if desc != None:
            return f"\n{Fore.WHITE}<{color}%s %s %s {Fore.WHITE}%s  @ %s  // .........%s......... (%s/%s) ................ || [%s and %s]>\n{color}%s{Fore.WHITE}" % (self.first.id, self.type, self.second.id, self.degree, angle.toString(self.angle()), self.__aspectTypeString__(), getSignAndIncludeCusp(self.first), getSignAndIncludeCusp(self.second), self.elements[0], self.elements[1], desc)
        else:
            return f"\n{Fore.WHITE}<{color}%s %s %s{Fore.WHITE} %s  @ %s  // .........%s......... (%s/%s) ................ || [%s and %s]>" % (self.first.id, self.type, self.second.id, self.degree, angle.toString(self.angle()), self.__aspectTypeString__(), getSignAndIncludeCusp(self.first), getSignAndIncludeCusp(self.second), self.elements[0], self.elements[1])



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


# z (intensity) = f(orb, aspect_angle, elementaL_harmony, aspect_itself)
#TODO
    def intensity(self):
        pass

# Returns how harmonious the aspect is (Bool, Int)
# Example: trine --> (True, 3) (3 is the intensity)
    def harmony(self):



        if True: #self.name == ('Sun', 'Venus'):

            if self.type == const.CONJUNCTION:
                return 2
            if self.type == const.SEXTILE:
                return 1
            if self.type == const.TRINE:
                return 3


            if self.type == const.SQUARE:
                return -3
            if self.type == const.QUINCUNX:
                return -2
            if self.type == const.CONJUNCTION:
                return -1

            if self.type == const.NO_ASPECT:
                return 0

            else:
                if self.isHarmonious(): 
                    return 1
                else: 
                    return -1


    def harmonyValue_broken(self):
        # Should return a value between -1 and 1 

        value = 0 

        if self.elementalHarmony():
            value = 0.25 
            if self.type == aspectFromDeg(const.CONJUNCTION):
                value = 0.75 
            elif self.type == aspectFromDeg(const.SEXTILE):
                value = 0.5
            elif self.type == aspectFromDeg(const.TRINE):
                value = 1
            elif self.type == aspectFromDeg(const.SQUARE):
                value = 0
            elif self.type in self.disharmonious_aspects: 
                value = value*0.5
            else: 
                value = 0.25 
            return value 
            

        if self.elementalChallenge(): 
            value = -0.25

            if self.type == aspectFromDeg(const.SQUARE):
                value = -1 
            if self.type == aspectFromDeg(const.QUINCUNX):
                value =  -0.75
            if self.type == aspectFromDeg(const.OPPOSITION):
                value =  -0.5
            if self.type in self.harmonious_aspects: 
                value = value*0.5
            else:
                value = -0.25 
            return value 


    def harmonyValue(self): 

        if self.name == ('Sun', 'Sun'):
            if self.elementalHarmony(): 

                if self.type == aspectFromDeg(const.TRINE) and self.orb < 8.0:
                    return 1 
                if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 8.0:
                    return 1
                if self.type == aspectFromDeg(const.SEXTILE) and self.orb < 4.0:
                    return 0.75


                if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 8.0:
                    return 0
                if self.type == aspectFromDeg(const.SEMISEXTILE) and self.orb < 2.0:
                    return 0
                if self.type == aspectFromDeg(const.QUINCUNX) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.SQUARE) and self.orb < 3.0:
                    return 0



                if self.type in self.harmonious_aspects and self.orb < 3.0:
                    return 0.5 
                if self.type in self.disharmonious_aspects and self.orb < 3.0:
                    return 0
                else: 

                    if self.first.sign == self.second.sign: #same sign 
                        return 0.5
                    elif getElement(self.first, set_orb=0) ==  getElement(self.second, set_orb=0): #same element 
                        return 0.25
                    else: 
                        return 0.10 
                


            
            if self.elementalChallenge():


                if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 3.0:
                    return -0.50
                if self.type == aspectFromDeg(const.SEMISEXTILE) and self.orb < 2.0:
                    return -0.25
                if self.type == aspectFromDeg(const.QUINCUNX) and self.orb < 3.0:
                    return -0.75
                if self.type == aspectFromDeg(const.SQUARE) and self.orb < 3.0:
                    return -1


                if self.type == aspectFromDeg(const.TRINE) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.SEXTILE) and self.orb < 3.0:
                    return 0


        


                if self.type in self.harmonious_aspects and self.orb < 2.0:
                    return -0.25 
                if self.type in self.disharmonious_aspects and self.orb < 3.0:
                    return -0.5
                else: 

                    return -0.25  
                
        if self.name == ('Sun', 'Venus') or self.name == ('Venus', 'Sun'):
            if self.elementalHarmony(): 

                if self.type == aspectFromDeg(const.TRINE) and self.orb < 8.0:
                    return 1 
                if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 8.0:
                    return 1
                if self.type == aspectFromDeg(const.SEXTILE) and self.orb < 4.0:
                    return 0.75


                if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 8.0:
                    return 0
                if self.type == aspectFromDeg(const.SEMISEXTILE) and self.orb < 2.0:
                    return 0
                if self.type == aspectFromDeg(const.QUINCUNX) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.SQUARE) and self.orb < 3.0:
                    return 0



                if self.type in self.harmonious_aspects and self.orb < 3.0:
                    return 0.5 
                if self.type in self.disharmonious_aspects and self.orb < 3.0:
                    return 0
                else: 

                    if self.first.sign == self.second.sign: #same sign 
                        return 0.5
                    elif getElement(self.first, set_orb=0) ==  getElement(self.second, set_orb=0): #same element 
                        return 0.25
                    else: 
                        return 0.10 
                


            
            if self.elementalChallenge():


                if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 3.0:
                    return -0.50
                if self.type == aspectFromDeg(const.SEMISEXTILE) and self.orb < 2.0:
                    return -0.25
                if self.type == aspectFromDeg(const.QUINCUNX) and self.orb < 3.0:
                    return -0.75
                if self.type == aspectFromDeg(const.SQUARE) and self.orb < 3.0:
                    return -1


                if self.type == aspectFromDeg(const.TRINE) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.SEXTILE) and self.orb < 3.0:
                    return 0


        


                if self.type in self.harmonious_aspects and self.orb < 2.0:
                    return -0.25 
                if self.type in self.disharmonious_aspects and self.orb < 3.0:
                    return -0.5
                else: 

                    return -0.25  
          
        if self.name == ('Sun', 'Moon') or self.name == ('Moon', 'Sun'):
            if self.elementalHarmony(): 

                if self.type == aspectFromDeg(const.TRINE) and self.orb < 8.0:
                    return 1 
                if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 8.0:
                    return 1
                if self.type == aspectFromDeg(const.SEXTILE) and self.orb < 4.0:
                    return 0.75


                if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 8.0:
                    return 0
                if self.type == aspectFromDeg(const.SEMISEXTILE) and self.orb < 2.0:
                    return 0
                if self.type == aspectFromDeg(const.QUINCUNX) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.SQUARE) and self.orb < 3.0:
                    return 0



                if self.type in self.harmonious_aspects and self.orb < 3.0:
                    return 0.5 
                if self.type in self.disharmonious_aspects and self.orb < 3.0:
                    return 0
                else: 

                    if self.first.sign == self.second.sign: #same sign 
                        return 0.5
                    elif getElement(self.first, set_orb=0) ==  getElement(self.second, set_orb=0): #same element 
                        return 0.25
                    else: 
                        return 0.10 
                
            
            if self.elementalChallenge():


                if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 3.0:
                    return -0.50
                if self.type == aspectFromDeg(const.SEMISEXTILE) and self.orb < 2.0:
                    return -0.25
                if self.type == aspectFromDeg(const.QUINCUNX) and self.orb < 3.0:
                    return -0.75
                if self.type == aspectFromDeg(const.SQUARE) and self.orb < 3.0:
                    return -1


                if self.type == aspectFromDeg(const.TRINE) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 3.0:
                    return 0
                if self.type == aspectFromDeg(const.SEXTILE) and self.orb < 3.0:
                    return 0


        


                if self.type in self.harmonious_aspects and self.orb < 2.0:
                    return -0.25 
                if self.type in self.disharmonious_aspects and self.orb < 3.0:
                    return -0.5
                else: 

                    return -0.25  
          

    
        return 0 
        if self.name == ('Sun', 'Venus') or ('Sun', 'Venus'): 
            pass 

        if self.name == ('Sun', 'Moon') or ('Moon', 'Sun'): 
            pass

        if self.name == ('Sun', 'Mars') or ('Sun', 'Mars'):
            pass  #more so chemistry / physical attraction 
            


    def isAspect(self): 
        """ Returns true if the aspect is within orb. """
        if self.type == aspectFromDeg(const.NO_ASPECT): 
            return False

        if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 8.0: 
            return True
        if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 8.0: 
            return True
        if self.type == aspectFromDeg(const.TRINE) and self.orb < 8.0: 
            return True 
        if self.type == aspectFromDeg(const.SEXTILE) and self.orb < 4.0: 
            return True 
        if self.type == aspectFromDeg(const.SQUARE) and self.orb < 7.0: 
            return True 
        if self.type == aspectFromDeg(const.QUINCUNX) and self.orb < 4.0:
            return True 
        if self.type == aspectFromDeg(const.SEMISEXTILE) and self.orb < 2.0:
            return True
        if self.type != aspectFromDeg(const.NO_ASPECT) and self.orb < 1.5: 
            return True 

        return False 
        

        
    # Returns if the aspect is `traditionally` harmonious.
    def isHarmonious(self):
        if self.type in DetailedAspect.harmonious_aspects and self.elementalHarmony():
            return True
        elif self.type == aspectFromDeg(const.NO_ASPECT):
            return self.elementalHarmony()
        elif (self.type not in DetailedAspect.harmonious_aspects and self.type != aspectFromDeg(const.NO_ASPECT)) and not self.elementalHarmony():
            return False
        elif (self.type not in DetailedAspect.harmonious_aspects and self.type != aspectFromDeg(const.NO_ASPECT)) and self.elementalHarmony(): 
            return True 
        else:
            return False


    # Example: Water/Water , Fire/Air, Fire/Fire all return true 
    # except if signs are opposite each other it'll return false 
    def elementalHarmony(self):

        if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 8.0:
            return False
        (element1, element2) = (getElement(self.first, set_orb=0), getElement(self.second, set_orb=0))

        if element1 == element2:
            return True

        if (element1, element2) == ('Water', 'Fire') or (element1, element2) == ('Fire', 'Water'):
            return False

        if (element1, element2) == ('Water', 'Air') or (element1, element2) == ('Air', 'Water'):
            return False

        if (element1, element2) == ('Earth', 'Air') or (element1, element2) == ('Air', 'Earth'):
            return False
        
        if (element1, element2) == ('Earth', 'Fire') or (element1, element2) == ('Fire', 'Earth'):
            return False

        return True

    # returns opposite of elementary harmony
    def elementalChallenge(self):
        return not self.elementalHarmony()


    # Returns if the aspect is `traditonally` challenging.
    # NOTE - we use the term `traditionally `
    def isChallenging(self):
        if self.type == aspectFromDeg(const.NO_ASPECT):
            return None
        else:
            return not (self.isHarmonious())


    #Returns a number of 
    def loveHarmony(self): 
        pass 


    

# Provides an interpretation of this particular aspect, None if there is none.
    def interpret(self):



        description = None

        # Sun Sun aspect
        if self.name == ('Sun', 'Sun'):
            description = ""

            SUN1 = self.first_planet_owner.name
            SUN2 = self.second_planet_owner.name

            if self.isHarmonious():

                if self.type == aspectFromDeg(const.TRINE):
                    description += f"{SUN1} and {SUN2} have much harmony between their core personalites and identities.\n"
                    description += f"{SUN1} and {SUN2} appreciate much about each other and understand each other.\n"
                    description += f"{SUN1} and {SUN2} understand each other's outlook on life.\n"
                    description += f"{SUN1} and {SUN2} have very similar outlooks and personalities, but enough compatible differences to be interesting.\n"

                if self.type == aspectFromDeg(const.SEXTILE):
                    description += f"{SUN1}  {SUN2} have a mutally beneficial personality.\n"
                    description += f"{SUN1} and {SUN2} appreciate much about each other and understand each other.\n"
                    description += f"{SUN1} and {SUN2} understand each other's outlook on life.\n"
                    description += f"{SUN1} and {SUN2} have extremely different outlooks on life, but it's not at all frictional.\n"

                if self.type == aspectFromDeg(const.CONJUNCTION):
                    description += f"{SUN1} and {SUN2} have similiar identities and characteristics.\n"
                    description += f"It's easy for {SUN1} and {SUN2} to be together.\n"
                    description += f"There is an innate understanding and appreciation between {SUN1} and {SUN2}\n"


            if self.isChallenging():
                description += f"{SUN1} and {SUN2} can have strong reactions towards each other... whether good or bad.\n"
                description += f"There can be ego conflicts between {SUN1} and {SUN2} due to a clash in personality identities.\n"
                description += f"There has to be much acceptance and understanding for things to work between {SUN1} and {SUN2}.\n"

                if self.type == aspectFromDeg(const.SQUARE):
                    description += f"There is a significant challenge due conflicting core identities between {SUN1} and {SUN2}.\n"
                    description += f"{SUN1} and {SUN2} can fall out over what appear to be simple things because of conflicting identities.\n"
                    description += f"Feelings of love because {SUN1} and {SUN2} can easily turn to hate.\n"
                    description += f"{SUN1} and {SUN2}'s core personalities are not ideal for a lasting , harmonious relationship with each other.\n"

                if self.type == aspectFromDeg(const.OPPOSITION):
                    description += f"{SUN1} and {SUN2} have opposite personalities, but it can be the root of either attraction or hatred. This can tip in one or the other direction.\n"
                    description += f"Though {SUN1} and {SUN2} are complete opposites, all is not loss and this can be a complimentary opposite.\n"
                    description += f"{SUN1} and {SUN2} can easily lean towards a love-hate relationship.\n"

        # Moon Moon aspect, if most exact, main theme is harmony
        if self.name == ('Moon', 'Moon'):
            description = ""

            MOON1 = self.first_planet_owner.name
            MOON2 = self.second_planet_owner.name

            if self.isHarmonious():
                description += f"{MOON1} and {MOON2} have similar tastes and emotional sensibilities."
                description += f"{MOON1} and {MOON2} feel comfortable with each other."
                description += f"{MOON1} and {MOON2} can easily create a safe, secure, and cozy home environment."

                if self.type == aspectFromDeg(const.TRINE):
                    description += f"{MOON1} and {MOON2} can intuitively sense each other's emotional and romantic needs."
                    description += f"{MOON1} and {MOON2} have an easy emotional flow of haromony and companionship."

            if self.isChallenging():
                description += f"{MOON1} and {MOON2} have difficulty being in sync emotionally."

                if self.type == aspectFromDeg(const.SQUARE):
                    description += f"It can be very hard for {MOON1} and {MOON2} to relate to each other emotionally."

                if self.type == aspectFromDeg(const.OPPOSITION):
                    description += f"{MOON1} and {MOON2} have complete opposite ways of expressing emotion but it can sometimes be complimentary as much challenging."

                # Sun Venus aspect

        if self.name == ('Mercury', 'Mercury'):
            description = ""

            MERCURY1 = self.first_planet_owner.name
            MERCURY2 = self.second_planet_owner.name

            if self.isHarmonious():
                description += f"{MERCURY1} and {MERCURY2} communicate in similar ways."

                if self.type == aspectFromDeg(const.CONJUNCTION):
                    description += f"{MERCURY1} and {MERCURY2} speak and think is very similar ways."
                    description += f"{MERCURY1} and {MERCURY2} approach problem solving in similar ways."
                    description += f"{MERCURY1} and {MERCURY2} have good chemistry and little confusion on what each other meant when they speak."

                if self.type == aspectFromDeg(const.TRINE):
                    description += f"There is much harmony between how {MERCURY1} and {MERCURY2} communicate and speak."
                    description += f"{MERCURY1} and {MERCURY2} approach problems in similar and complementary ways."
                    description += f"{MERCURY1} and {MERCURY2} enjoy talking to each other and sharing ideas."

            if self.isChallenging():
                description += f"{MOON1} and {MOON2} have difficulty being in sync emotionally."

                if self.type == aspectFromDeg(const.SQUARE):
                    description += f"It can be very hard for {MOON1} and {MOON2} to relate to each other emotionally."

                if self.type == aspectFromDeg(const.OPPOSITION):
                    description += f"{MOON1} and {MOON2} have complete opposite ways of expressing emotion but it can sometimes be complimentary as much challenging."

                # Sun Venus aspect



        if self.name == ('Venus', 'Venus'):
            description = ""

            VENUS1 = self.first_planet_owner.name
            VENUS2 = self.second_planet_owner.name

            if self.isHarmonious():
                description += f"{VENUS1} and {VENUS2} appreciate how each other expresses and receives love.\n"
                description += f"{VENUS1} and {VENUS2} like each other's tastes, decoration, and dressing styles.\n"
                description += f"{VENUS1} and {VENUS2} have similiar values which can help with decision making together.\n"
                description += f"There is ease and harmony when {VENUS1} and {VENUS2} are together.\n"

                if self.type == aspectFromDeg(const.CONJUNCTION):
                    description += f"{VENUS1} and {VENUS2} tend to like the same things and view love the same way.\n"
                    description += f"{VENUS1} and {VENUS2} likely have initial attraction.\n"
                    description += f"{VENUS1} and {VENUS2} may like the same clothing, decoration, and dressing styles.\n"
                    description += f"{VENUS1} and {VENUS2} have similar definitions of beauty.\n"

                if self.type == aspectFromDeg(const.TRINE): #Seen in friends/business partners as well
                    description += f"{VENUS1} and {VENUS2} perceive love in very similar and compatible ways.\n"
                    description += f"{VENUS1} and {VENUS2} feels very comfortable around each other.\n"
                    description += f"{VENUS1} and {VENUS2} may like similar clothing, decoration, and dressing styles.\n"
                    description += f"{VENUS1} and {VENUS2} have similar definitions of beauty.\n"
                    description += f"{VENUS1} and {VENUS2} have much harmony together and good romantic capability.\n"
                    description += f"{VENUS1} and {VENUS2} help each other discover new things each other would like.\n"

                if self.type == aspectFromDeg(const.SEXTILE): # good friendship
                    description += f"{VENUS1} and {VENUS2} have supporting loving styles.\n"
                    description += f"{VENUS1} and {VENUS2} have compatible loving styles that may not always be apparent, but not at all disharmonious.\n"
                    description += f"{VENUS1} and {VENUS2} have good friendship with one another.\n"
                    description += f"{VENUS1} and {VENUS2} may have different clothing styles, decoration, and ways of showing love but they are not at all incompatible.\n"


            if self.isChallenging():
                description += f"{VENUS1} and {VENUS2} have different values when it comes to love which becomes more and more obvious over time.\n"
                description += f"{VENUS1} and {VENUS2} have disimilar ways of expressing and receiving love in very important ways.\n"
                description += f"{VENUS1} and {VENUS2} likely do not know how to instinctively please each other.\n"
                description += f"{VENUS1} and {VENUS2} can easily argue over basic taste and their incompatible social lives.\n"
                description += f"{VENUS1} and {VENUS2} have dissimilar ways of managing money which can cause issues.\n"

                if self.type == aspectFromDeg(const.OPPOSITION):
                    description += f"{VENUS1} and {VENUS2} may feel a strong connection right away, opposites attract.\n"
                    description += f"{VENUS1} and {VENUS2} can easily develop a natural bond.\n"
                    description += f"{VENUS1} and {VENUS2} have opposite ways of expressing love that will cause tension overtime.\n"
                    description += f"Though {VENUS1} and {VENUS2} may have strong attraction, they will find eventually they don't have a lot in common in regards to ideas of beauty.\n"
                    description += f"{VENUS1} and {VENUS2} have strong sexual attraction due to the friction caused by being opposites.\n"

                if self.type == aspectFromDeg(const.SQUARE):
                        description += f"{VENUS1} and {VENUS2} have intense attraction that falsely feels like a soulmate connection.\n"
                        description += f"Over time, {VENUS1} and {VENUS2} will find they have troublesome differences with how each other views and accepts love.\n"
                        description += f"{VENUS1} and {VENUS2} will have much difficulty overtime due to inherit incompatbilites with how love is viewed and expressed.\n"
                        description += f"{VENUS1} and {VENUS2} see beauty and love in very different, inharmonious ways.\n"





        if self.name == ('Sun', 'Venus'):
            description = ""

            SUN = self.first_planet_owner.name
            VENUS = self.second_planet_owner.name


            if self.isHarmonious():
                description += f"There is some harmony and common interest between {SUN} and {VENUS}.\n"
                description += f"{SUN} feels more loving in {VENUS}'s presence.\n"
                description += f"{VENUS} thinks {SUN} is charming and interesting.\n"
                description += f"{VENUS} admires and wants to please {SUN}.\n"
                description += f"There is a pleasing and supportive attraction between {VENUS} and {SUN}.\n"
                description += f"{SUN} and {VENUS} agree on how to save and spend money.\n"

                if self.type == aspectFromDeg(const.TRINE):
                    description += f"{SUN} and {VENUS} truly value each other.\n"

                if self.type == aspectFromDeg(const.CONJUNCTION):
                    description += f"{SUN} and {VENUS} like a lot of things about each other.\n"

                if self.type == aspectFromDeg(const.SEXTILE):
                    description += f"{SUN} and {VENUS} have mutual respect for each other and see value.\n"


            if self.isChallenging():
                description += f"{VENUS}'s value system conflicts with {SUN}'s outlook on life and life path.\n"
                description += f"{SUN} and {VENUS} will like each other one day and then be fustrasted with each other the next.\n"
                description += f"{VENUS} may resent {SUN} because {VENUS} tries to please {SUN}, getting nothing in return.\n"
                description += f"{SUN} may not appreciate {VENUS}.\n"
                description += f"{VENUS} may be taken for granted.\n"

                if self.type == aspectFromDeg(const.SQUARE):
                    description += f"Relationship looks promising in the beginning but fails to meet expectations.\n"
                    description += f"There is unequal give/take between {SUN} and {VENUS}.\n"
                    description += f"{VENUS} resorts to playing games because the scales are unbalanced.\n"
                    description += f"When one gives, the other feels obligated to give in return.\n"
                    description += f"If {SUN} and {VENUS} separate love can easily turn to hate.\n"

                if self.type == aspectFromDeg(const.OPPOSITION):
                    description += f"There is some challenge and a chase but potentially can be rewarding. Not very problematic.\n"



        return description



# reads interpretation from cvs file
    def interpretation(self):
        # Load the csv file
        try:
            import pandas as pd
            df = pd.read_csv('astrology/interpretations.csv')
            df.set_index('ASPECT', inplace=True)
        except:
            return

        (p1, p2) = self.name
        aspect_name = f'{p1}_{p2}'
        aspect_angle = self.type  #TRINE, CONJUNCTION, etc


        try:
            description = df.loc[aspect_name, aspect_angle]

            # Replaces the place holders with their names

            if p1 == p2:
                x = description.replace(f'{p1}1', self.first_planet_owner.name)
                y = x.replace(f'{p2}2', self.second_planet_owner.name)
            else:
                x = description.replace(p1, self.first_planet_owner.name)
                y = x.replace(p2, self.second_planet_owner.name)


            return y.strip()
        except:
            return ''





# For ALGORITHM ===============================================================

    def isLoving(self): 
        """Returns whether the aspect contributes to mutual harmonious love or not. 
        -1 = not loving (a killer) , 0 = neutral, 1 = loving (a creator) . 
        Greater leeway  for orbs is given for the same planets (e.g. Sun-Sun) than for different planets (e.g. Sun-Moon)."""

        if self.name == ('Sun', 'Sun'):
            if self.elementalHarmony():
                return 1
            else:
                return -1
            


        if self.name == ('Moon', 'Moon'):
            if self.elementalHarmony():
                return 1
            else:
                return -1


        if self.name == ('Venus', 'Venus'):
            if self.elementalHarmony():
                return 1
            else:
                return -1


        if self.name == ('Mars', 'Mars'):
            if self.elementalHarmony():
                return 1
            else:
                return -1

        if self.name == ('Mars', 'Saturn') or self.name == ('Saturn', 'Mars'):
            if self.isAspect():
                if self.elementalHarmony(): 
                    if self.type == aspectFromDeg(const.OPPOSITION):
                        return -1
                    else: 
                        return 0
                else :
                    return -1
            else:
                return 0

        # Sun aspects

        if self.name == ('Sun', 'Moon') or self.name == ('Moon', 'Sun'):
            if self.isAspect():
                if self.elementalHarmony(): 
                    return 1
                else :
                    return -1
            else:
                return 0

        if self.name == ('Sun', 'Venus') or self.name == ('Venus', 'Sun'):
            if self.isAspect():
                if self.elementalHarmony(): 
                    return 1
                else :
                    return -1
            else:
                return 0
        
        if self.name == ('Sun', 'Mars') or self.name == ('Mars', 'Sun'):
            if self.isAspect():
                if self.elementalHarmony(): 
                    return 1
                else :
                    return -1
            else:
                return 0

        if self.name == ('Venus', 'Mars') or self.name == ('Mars', 'Venus'):
            if self.isAspect():
                if self.type == aspectFromDeg(const.OPPOSITION):
                    return 1
                if self.elementalHarmony(): 
                    return 1
                else :
                    return -1
            else:
                return 0

        if self.name == ('Moon', 'Mars') or self.name == ('Mars', 'Moon'):
            if self.isAspect():
                if self.type == aspectFromDeg(const.OPPOSITION):
                    return -1
                if self.type == aspectFromDeg(const.SQUARE):
                    return -1
                if self.elementalHarmony(): 
                    return 1
                else :
                    return -1
            else:
                return 0

        if self.name == ('Sun', 'Jupiter') or self.name == ('Jupiter', 'Sun'):
            if self.isAspect():
                return 1
            else:
                return 0

        if self.name == ('Venus', 'Jupiter') or self.name == ('Jupiter', 'Venus'):
            if self.isAspect():
                return 1
            else:
                return 0

        if self.name == ('Sun', 'Saturn') or self.name == ('Saturn', 'Sun'):
            if self.isAspect():
                if self.elementalHarmony(): 
                    return 1
                else:
                    return -1
            else:
                return 0


        # Moon aspects

        if self.name == ('Moon', 'Venus') or self.name == ('Venus', 'Moon'):
            if self.isAspect():
                if self.elementalHarmony(): 
                    return 1
                else:
                    return -1
            else:
                return 0

        if self.name == ('Asc', 'North Node') or self.name == ('North Node', 'Asc'):
            if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 11:
                return 1 

        return 0 
           
    def isAttracted(self):


        if self.name == ('Mars', 'Mars'):
            if self.isAspect():
                if self.type == aspectFromDeg(const.QUINCUNX) or self.type == aspectFromDeg(const.SEMISEXTILE):
                    return -1
                else: 
                    return 1
            else: 
                return 0 

        if self.name == ('Venus', 'Mars') or self.name == ('Mars', 'Venus'):
            if self.isAspect():
                return 1
            else:
                return 0

        if self.name == ('Moon', 'Uranus') or self.name == ('Uranus', 'Moon'):
            if self.isAspect():
                return 1
            else:
                return 0

        if self.name == ('Sun', 'Asc') or self.name == ('Asc', 'Sun'):
            if self.type == aspectFromDeg(const.OPPOSITION): 
                return 1
            else: 
                return 0

        if self.name == ('Sun', 'Mars') or self.name == ('Mars', 'Sun'):
            if self.isAspect():
                return 1

        if self.name == ('Sun', 'Pluto') or self.name == ('Pluto', 'Sun'):
            if self.isAspect():
                return 1

        if self.name == ('Moon', 'Mars') or self.name == ('Moon', 'Mars'):
            if self.isAspect():
                return 1

        if self.name == ('Venus', 'North Node') or self.name == ('North Node', 'Venus'):
            if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 11:
                return 1
            if self.type == aspectFromDeg(const.SEXTILE):
                return 1
            if self.type == aspectFromDeg(const.TRINE) and self.orb < 9:
                return 1
            if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 11:
                return 1
            if self.type == aspectFromDeg(const.SQUARE) and self.orb < 6:
                return 1

        if self.name == ('Moon', 'North Node') or self.name == ('Moon', 'Venus'):
            if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 11:
                return 1

        if self.name == ('Moon', 'South Node') or self.name == ('South Node', 'Moon'):
            if self.type == aspectFromDeg(const.CONJUNCTION) and self.orb < 11:
                return 1

        if self.name == ('Venus', 'Asc') or self.name == ('Asc', 'Venus'): 
            if self.isAspect(): 
                if self.type != aspectFromDeg(const.SQUARE) and self.type != aspectFromDeg(const.QUINCUNX) and self.isHarmonious():
                    return 1
            
        return 0

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
        for aspect in self.list:
            s += "\n" + aspect.__str__()

        return s

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return (x for x in self.list)

    def sort(self):
        self.list = sorted(self.valid().list, key=lambda x: x.orb, reverse=False)
    ## Gets a particular aspect, example: Mars/Venus aspect --> get('Mars', 'Venus')
    ##TODO: confirm , I think planet 1 is the outer chart's planet. (self) object
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

    def toDict(self):
        aspectDic = {}
        if self != None:
            for aspect in self:
                id = f"{aspect.name[0]} {aspect.name[1]}"
                aspectDic[id] = aspectToDict(aspect)
        return aspectDic

    def toArray(self):
        dictOfObjects = self.toDict()
        array = []
        for obj_name in dictOfObjects:
            this_object = dictOfObjects[obj_name]
            this_object['name'] = obj_name
            array.append(this_object)
        return array






# Utility Functions for algoritm and calculations

# Returns the sun sign of a given date where time is a datetime float 
def getASun(time):
    from database.user import User
    from database.Location import Location
    from datetime import datetime
    loc = Location(latitude=40.7, longitude=-74.0) 
    user = User(do_not_fetch=True, name="micheal", birthday = datetime.fromtimestamp(float(time)), known_time=True, hometown=loc)
    return user.sun 
    

# Returns a list of planets for each degree of the sign (0-29)
def getAllDegreesForSign(sign, startAt):
    planets = []
    degrees = [i for i in range(0,29+1)]
    degreesWeHave = []

    time = startAt
    sun = getASun(time)
    while sun.sign == sign:
        if int(sun.signlon) not in degreesWeHave:
            degreesWeHave.append(round(sun.signlon, 0))
            planets.append(sun)
            #print("ADDING DEGREE " + str(sun.signlon))
        time = time+900
        sun = getASun(time)
    #print(("\n\nStopped at : " + str(time)))
    return planets 
       



# Gets the possible aspects a particular sign can make with another planet 
#placements : an array of planets . where each planet is  a particular sign in each degree
def getAllPossibleAspectsWithSigninEachDegree(placements, planet):
    aspects = []
    for p in placements:
        aspect = DetailedAspect(p, planet, aspectsToGet=const.ALL_ASPECTS)
        aspects.append(aspect)
    return aspects #an array of aspects that the planet can make with each degree of the sign
    

def aspectsToHarmonies(aspects): 
    """Accepts an array of aspects and returns an array of harmony scores"""
    scores = []
    for asp in aspects:
        scores.append(asp.harmonyValue()) 
    return scores
     

def bestFitSunSignForPlanets(planets, mode='default'): 
    from astrology.Constants import everySun
    import numpy as np 
    """Given planets, say, the user's natal chart (ex: Sun in Cancer, Moon in Scorpio, ... , etc) 
    This function will return the best fit sun sign for the user's natal chart.
    It will compute the harmony scores for each sun sign and return the rank for each aspect """


    mySunTheirSunWeight = 0.5
    myMoonTheirSunWeight = 0.25
    myVenusTheirSunWeight = 0.25

    if mode=='equal': 
        mySunTheirSunWeight = myMoonTheirSunWeight = myVenusTheirSunWeight = 1.0

    if mode == 'venus': 
        mySunTheirSunWeight = 0.25
        myMoonTheirSunWeight = 0.25
        myVenusTheirSunWeight = 0.5

    totals = []

    harmonyScoresWithMySunSign = []
    harmonyScoresWithMyMarsSign = []
    harmonyScoresWithMyVenusSign = []

    mySun = None
    myMoon = None
    myVenus = None 
    
    for planet in planets: 
        if planet.id == "Sun":
            mySun = planet
        if planet.id == "Moon":
            myMoon = planet
        if planet.id == "Venus":
            myVenus = planet
        #howEachSignInteractsWithMyPlanet =  getAllPossibleAspectsWithSigninEachDegree(everySun, planet)
        #harmonyScores = aspectsToHarmonies(howEachSignInteractsWithMyPlanet)
        #totals.append(harmonyScores)

    
    howEachSignInteractsWithMySun = getAllPossibleAspectsWithSigninEachDegree(everySun, mySun)
    harmonyScoresWithMySunSign = aspectsToHarmonies(howEachSignInteractsWithMySun)
    harmonyScoresWithMySunSign = [element * mySunTheirSunWeight for element in harmonyScoresWithMySunSign]
    totals.append(harmonyScoresWithMySunSign)

    howEachSignInteractsWithMyMoon = getAllPossibleAspectsWithSigninEachDegree(everySun, myMoon)
    harmonyScoresWithMyMoonSign = aspectsToHarmonies(howEachSignInteractsWithMyMoon)
    harmonyScoresWithMyMoonSign = [element * myMoonTheirSunWeight for element in harmonyScoresWithMyMoonSign]
    totals.append(harmonyScoresWithMyMoonSign)

    howEachSignInteractsWithMyVenus = getAllPossibleAspectsWithSigninEachDegree(everySun, myVenus)
    harmonyScoresWithMyVenusSign = aspectsToHarmonies(howEachSignInteractsWithMyVenus)
    harmonyScoresWithMyVenusSign = [element * myVenusTheirSunWeight for element in harmonyScoresWithMyVenusSign]
    totals.append(harmonyScoresWithMyVenusSign)

       

    totals = np.array(totals, dtype=object)
    #allScores = np.add(0, totals.sum(axis=0))
    sums = np.sum(totals, axis=0)

    results = {} 
    for sun, score in zip(everySun, sums):
        info = f"Sun in {sun.sign}, {int(sun.signlon)} deg"
        results[info] = score 
        
    orderdResults = {k: v for k, v in sorted(results.items(), key=lambda item: item[1])}

    return orderdResults 
    


def bestSunsForLove(person):
    from astrology.Constants import everySun

    loveScoresForEachSun = []

    for sun in everySun: 
        scores = person.singlePlacementLoveSynastry(sun)
        scores.append(sun)
        loveScoresForEachSun.append(scores)

    return sortList(loveScoresForEachSun)

def bestSunsForSex(person):
    from astrology.Constants import everySun

    loveScoresForEachSun = []

    for sun in everySun: 
        scores = person.singlePlacementSexSynastry(sun)
        scores.append(sun)
        loveScoresForEachSun.append(scores)

    return sortList(loveScoresForEachSun)


def printBestSunsList(bestSunsList):
    for info in bestSunsList:
        posAsp = info[3]
        negAsp = info[4]
        print(f"{info[-1].sign} {info[-1].signlon} : Total: {info[2]} ----> Negative Placements: {info[1]} ----> Positive Placements: {info[0]}\n")
        for asp in posAsp: 
            print(asp) 
        for asp in negAsp: 
            print(asp) 
        print("\n\n\n\n\n\n\n\n")


#sorts a list of lists by the 3rd element in each list
def sortList(list):
    list.sort(key=lambda x: x[2])
    return list












""""
#Represents a pair of users, used to run synastry and get aspects.
class Pairing:

    def __init__(self, user1, user2, aspectsToGet=const.ALL_ASPECTS):
        self.user1 = user1
        self.user2 = user2
        self.all = user1.aspects(user2, aspectsToGet=aspectsToGet)   #Gets the aspects between two users (all of them)
        self.aspects = validAspects(self.all)                  # Returns all 'real' aspects.

"""
