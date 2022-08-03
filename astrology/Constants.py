from astrology.NatalChart import * 
from database.user import User 
from database.Location import Location
from datetime import datetime 
import pytz

loc=Location(latitude=float(32.2988), longitude=float(-90.1848))
micheal = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(932604720), known_time=True, hometown=loc)
micheal.natal()

loc2=Location(latitude=float(34.0007), longitude=float(-81.0348))
gracen = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(881837400), known_time=True, hometown=loc2)
gracen.natal()

chicago=Location(latitude=float(42.2586), longitude=float(-87.8406))
hirsch = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(914023440), known_time=True, hometown=chicago)
hirsch.natal()

sahilTimestamp = 926604000
fahidTimeStamp = 940656660
atlanta=Location(latitude=float(33.7490), longitude=float(-84.3880))
belAirMd=Location(latitude=float(39.5359), longitude=float(-76.3483))

sahil = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(sahilTimestamp), known_time=True, hometown=belAirMd)
sahil.natal()

fahid = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(fahidTimeStamp), known_time=True, hometown=atlanta)
fahid.natal()





# Returns a list of the Capricon Suns in ALL degrees
def listOfCapricornSuns_all_degrees():
    startAt=-843375
    suns =  getAllDegreesForSign('Capricorn', startAt)
    #suns.pop()
    return suns 
    
allCapricornSuns = listOfCapricornSuns_all_degrees()

allAquariusSuns = getAllDegreesForSign('Aquarius', 1700925)

allPiscesSuns = getAllDegreesForSign('Pisces', 4257825)

allAriesSuns = getAllDegreesForSign('Aries', 6846985)

allTaurusSuns = getAllDegreesForSign('Taurus', 9479710)

allGeminiSuns = getAllDegreesForSign('Gemini', 12152240)

allCancerSuns = getAllDegreesForSign('Cancer', 14859770)

allLeoSuns = getAllDegreesForSign('Leo', 17577500)

allVirgoSuns = getAllDegreesForSign('Virgo', 20280930)

allLibraSuns = getAllDegreesForSign('Libra', 22949960)

allScorpioSuns = getAllDegreesForSign('Scorpio', 25574690)

allSagittariusSuns = getAllDegreesForSign('Sagittarius', 28160720.0)

everySun = allCapricornSuns + allAquariusSuns + allPiscesSuns + allAriesSuns + allTaurusSuns + allGeminiSuns + allCancerSuns + allLeoSuns + allVirgoSuns + allLibraSuns + allScorpioSuns + allSagittariusSuns