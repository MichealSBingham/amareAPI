# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



import xml4h
from database.user import User
from flatlib.geopos import GeoPos
import bs4
import julian
import datetime

#name of xml file
filename = 'c_sample.xml'

#loads documents
_doc = xml4h.parse(filename)
doc = _doc.child('astrodatabank_export')
entries = doc.adb_entry # this will contain all of the entries of each person in the database

users = []
errors = []
def readGender(gender):
    if gender == 'M':
        return 'male'
    elif gender == 'F':
        return 'female'
    elif gender == 'MF':
        return 'transfemale'
    elif gender == 'FM':
        return 'transmale'
    else:
        return 'non_binary'

def readTimeKnown(rr):
    if rr == 'A' or  rr == 'AA' or rr =='B':
        return True
    elif rr == 'X':
        return False
    else:
        raise Exception('RoddenRating is not what we want. ')


from bs4 import BeautifulSoup
import requests

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='


def return_image(title):
    import wikipedia
    import json

    try:

        page = wikipedia.page(title)
        wikipedia.set_lang('en')
        title = page.title
        response = requests.get(WIKI_REQUEST + title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']

        return img_link
    except Exception as e:
        print(f"Could not get image {e}")
        raise Exception("Could not get image ")


def errorFromNumber(number):
    if number == 0:
        return 'Not a public figure.'
    elif number == 2:
        return '2nd'
    elif number == 3:
        return '3rd'
    else:
        return f'{number}th'
#Reads a single entry and convets it to a user object
def readOne(entry):

    import re
    from database.Location import Location
    from datetime import datetime

  
    #assert (entry.public_data.datatype['dtc'] == '1'), print('Skipping ... Not a public figure ')
    
    #Making sure that the entry is a public figure 
    if not (entry.public_data.datatype['dtc'] == '1'):
        raise ValueError(0, 'Not a public figure.')

    #assert entry.public_data.bdata.sbdate['ccalendar'] == 'g', print(f"{name}: This is not given in the Gregorian Calendar")

    #Getting basic information about the person
    name = entry.public_data.sflname.text
    
    #Making sure that this is given in the Gregorian Calendar
    if not (entry.public_data.bdata.sbdate['ccalendar'] == 'g'):
        raise ValueError(1, f"{name}: This is not given in the Gregorian Calendar")




    
    gender = readGender(entry.public_data.gender.text)
    try: 
        knownTime = readTimeKnown(entry.public_data.roddenrating.text)
    except:
        knownTime = False 

    try:
        timeUnknown = bool(entry.public_data.bdata.sbtime["time_unknown"])
    except:
        timeUnknown = False

    knownTime = not timeUnknown

    lat = entry.public_data.bdata.place['slati']
    long = entry.public_data.bdata.place['slong']

    if len(re.split('(\D)',lat)[-1]) > 2:
        lat = lat[:-2]

    if len(re.split('(\D)', long)[-1]) > 2:
        long = long[:-2]

    pos = GeoPos(lat, long)

    hometown = Location(latitude=pos.lat, longitude=pos.lon)




    
    


    year = entry.public_data.bdata.sbdate['iyear']
    month = entry.public_data.bdata.sbdate['imonth']
    day = entry.public_data.bdata.sbdate['iday']

    datestring = entry.public_data.bdata.sbdate_dmy.text
    timestring = entry.public_data.bdata.sbtime["sbtime_ampm"]

    if timestring == "":
        timestring = "12:00 PM"
    if 'noon' in timestring:
        timestring = "12:00 PM"

    #Getting the julian time of the date
    jd = float(entry.public_data.bdata.sbtime["jd_ut"])
    dt = julian.from_jd(jd, fmt='jd')

    #This is broken so we will use the julian date instead
    #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    #dt = datetime.strptime(f'{year}-{month}-{day} {timestring}', '%Y-%m-%d %I:%M %p')
    #print(f"{name}'s birthday is ", dt)

    #timestamp = hometown.timezone().localize(dt, is_dst=None)
    #print(f"the timestamp from {name} is ", timestamp)








    profile_image = None


#    try:
 #       wikilink = entry.text_data.wikipedia_link.text.split('#')[0]
  #      paths = wikilink.split('/')
   #     title = paths[-1]

    #    profile_image = return_image(title)
   # except Exception as e:
   #     print(f"Cannot get because of error {e}")


    try:
        bio = entry.text_data.shortbiography.text
    except Exception as e:
        bio = None
        


  

    try:
        cats = entry.research_data.categories.category
        research_notes = []
        for cat in cats:
            c = cat.text #example: Family : Parenting : Kids -Traumatic event
            id = cat['cat_id']

            if id == '518' or id == '519':
                isPhysicistOrMathematician = True
                isScientist = True 

            if int(id) >= 513 and int(id) < 519:
                isScientist = True

            temp_notes = c.split(':')  # will return ['Family ', ' Parenting ', ' Kids -Traumatic event']
            notes = []
            for note in temp_notes:
                notes.append(note.replace('/', '^').strip())
            research_notes.append(':'.join(notes))
    except Exception as e:
        research_notes = None
        print(f"Cannot get notes from {name} because of error {e}")





    return User(do_not_fetch=True,
                is_notable=True,
                name=name,
                known_time=knownTime,
                skip_getting_natal=True,
                hometown=hometown,
                birthday=dt,
                sex=gender,
                username=''.join(name for name in name if name.isalnum()),
                profile_image_url=profile_image,
                orientation=[],
                bio=bio,
                notes=research_notes)




        





def main():
   
    non_scientists = get_non_scientists()
    scientists = get_scientists()
    print(f'Found {len(non_scientists)} non scientists')
    print(f'Found {len(scientists)} scientists')
 



def main2():
    import time
    start_time = time.time()
    err = 0

    print(f"We have {len(entries)} people in our database")
    interation = 0 

    for person in entries:
        interation += 1
        try:
            print(f"We are on iteration {interation} of {len(entries)}")
            p = readOne(person)
            users.append(p)
        except ValueError as error:
            err = err+1
            print(f"Error #{err} {error}")
            errors.append(err)
            continue

    print("--- %s seconds ---" % (time.time() - start_time))
    print(f"We have {len(users)} users in our database and {err} errors")




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/




# Helper Functions for reading the data

#Returns all of the entries in the database that are scientists 
def get_scientists():
    scientists = [] 
    for person in entries:
        try:
            p = readOne(person)
            if p.isMathematicianOrPhysicist:
                scientists.append(p)
        except Exception as error:
            print(f"Error {error}")
   
    return scientists

def get_non_scientists():
    non_scientists = []
    for person in entries:
        try: 
            p = readOne(person)
            if p.isNonScientist:
                non_scientists.append(p)
        except Exception as e:
            print(f"Error {e}")
    return non_scientists



# Returns the frequency of each sun sign in the natal chart of an array of users 
def get_sun_sign_frequency(users):
    sun_sign_frequency = {}
    for user in users:
        try: 
            user = user.readOne(user)
        except: 
            continue
        user.natal()
        sun_sign_frequency[user.sun.sign] = sun_sign_frequency.get(user.sun.sign, 0) + 1
    return sun_sign_frequency