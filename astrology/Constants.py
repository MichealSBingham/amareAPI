from astrology.NatalChart import * 
from database.user import User 
from database.Location import Location
from datetime import datetime 
import pytz

loc=Location(latitude=float(32.2988), longitude=float(-90.1848))
micheal = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(932604720), known_time=True, hometown=loc)
micheal.natal()

loc2=Location(latitude=float(34.0007), longitude=float(-81.0348))
gracen = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(881837400), known_time=True, hometown=loc)
gracen.natal()



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