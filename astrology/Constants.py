from astrology.NatalChart import * 
from database.user import User 
from database.Location import Location
from datetime import datetime 
import pytz

loc=Location(latitude=float(32.2988), longitude=float(-90.1848))
jacksonMS = loc 
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

westCovaCA=Location(latitude=float(34.0686), longitude=float(-117.9390))
zyla = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(847335540), known_time=True, hometown=westCovaCA)
zyla.natal()

zylasPerson=Location(latitude=float(34.7304), longitude=float(-86.5861))
zylasPerson = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(611583300), known_time=True, hometown=westCovaCA)
zylasPerson.natal()

kelle = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(335836800), known_time=True, hometown=loc)
kelle.natal()

maurice = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(255355200), known_time=True, hometown=loc)
maurice.natal()

boo = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(109872000), known_time=True, hometown=loc)
boo.natal()

oscarbday = -569656800
oscar = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(oscarbday), known_time=False, hometown=loc)
oscar.natal()

ouidsabday = -571212000
ouida = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(ouidsabday), known_time=False, hometown=loc)
ouida.natal()

sp=Location(latitude=float(-22.355), longitude=float(-47.3857)) 
biancabday = 698505000
bianca = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(biancabday), known_time=True, hometown=sp)


#san fran
pa=Location(latitude=float(37.4419), longitude=float(-122.1430)) 
aidanbday = 854991000
aidan = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(aidanbday), known_time=True, hometown=pa)
aidan.name = "Aidan"


tn=Location(latitude=float(35.1495), longitude=float(-90.0490)) 
nyamalbday = 881775000
nyamal = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(nyamalbday), known_time=True, hometown=pa)
nyamal.name = "Nyamal"


davidbday = 920196000
maryanbday = 815580000
sanDiego=Location(latitude=float(32.7157), longitude=float(-117.1611))
greensBoro=Location(latitude=float(36.0726), longitude=float(-79.7920))

david = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(davidbday), known_time=True, hometown=greensBoro)
maryan = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(maryanbday), known_time=False, hometown=sanDiego)



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