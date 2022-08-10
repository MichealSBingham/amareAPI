# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



from localdataset.scraping import getRelationships
import xml4h
from database.user import User
from flatlib.geopos import GeoPos
import bs4
import julian
import datetime
from database.user import *
from multiprocessing import Pool
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
warnings.filterwarnings('ignore', category=Warning, module='bs4')
from database.user import db 
import json 

#name of xml file
filename = 'celebData.xml'
celebNatalData = '_celebBirthData.json'

#loads documents
#_doc = xml4h.parse(filename)
#doc = _doc.child('astrodatabank_export')
#entries = doc.adb_entry # this will contain all of the entries of each person in the database

users = []
errors = []
disagreements = []

jsonData = {}
natalData = {}

data  = {} 


CELEBRELATIONSHIPS = []
errs = 0 


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
    elif rr == 'XX': 
        return False
    else:
        return False #raise Exception('RoddenRating is not what we want. ')


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
        #print("Could not get image because of error " + str(e))
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
    import pytz 
  
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
    #jd = float(entry.public_data.bdata.sbtime["jd_ut"])
    #dt = julian.from_jd(jd, fmt='jd')

    #This is broken so we will use the julian date instead
    #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    dt = datetime.strptime(f'{year}-{month}-{day} {timestring}', '%Y-%m-%d %I:%M %p')
    #print(f"{name}'s birthday is ", dt)

    try: 
        timestamp = hometown.timezone().localize(dt, is_dst=None).astimezone(pytz.UTC)
    except Exception as error: 
        print(f"Error in timestamp {error}")
        return None
        #raise Exception('Time not valid')
    #print(f"the timestamp from {name} is ", timestamp)


    if knownTime: 
        rising = entry.public_data.bdata.positions["asc_sign"]
    else: 
        rising = None 






    profile_image = None

        
    try:
        wikilink = entry.text_data.wikipedia_link.text.split('#')[0]
        paths = wikilink.split('/')
        title = paths[-1]

        profile_image = return_image(title)
    except Exception as e:
        profile_image = None 
        #print(f"Cannot get because of error {e}")

    

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
        #print(f"Cannot get notes from {name} because of error {e}")





    return User(do_not_fetch=True,
                is_notable=True,
                name=name,
                known_time=knownTime,
                skip_getting_natal=True,
                hometown=hometown,
                birthday=timestamp,
                sex=gender,
                username=''.join(name for name in name if name.isalnum()),
                profile_image_url=profile_image,
                orientation=[],
                bio=bio,
                notes=research_notes, 
                risingFromCelebDate=rising)


def readJustUrl(entry):
    if not (entry.public_data.datatype['dtc'] == '1'):
        raise ValueError(0, 'Not a public figure.')


    name = entry.public_data.sflname.text

    username = ''.join(name for name in name if name.isalnum())


    try:
        wikilink = entry.text_data.wikipedia_link.text.split('#')[0]
        paths = wikilink.split('/')
        title = paths[-1]

        #profile_image = return_image(title)
    except Exception as e:
        raise ValueError(1, "No link")
        profile_image = None

        
    return {"username": username, "wiki": wikilink}
    
def readJustBirthname(entry):
    if not (entry.public_data.datatype['dtc'] == '1'):
        raise ValueError(0, 'Not a public figure.')



    name = entry.public_data.sflname.text 

    username = ''.join(name for name in name if name.isalnum())


    try:
        birthName = entry.public_data.birthname.text
        

        #profile_image = return_image(title)
    except Exception as e:
        return  {"username": username, "birthName": None, "name": name}
      
        

        
    return {"username": username, "birthName": birthName, "name": name}
    
    

   


 
        



def getWikiLinks(): 
    import json 
    allLinks = {}
    noLinks = 0 
    links = 0 

    tot = len(entries)
    prog = 0 

    printProgressBar(0, tot, prefix = 'Progress:', suffix = 'Complete', length = 50)


    with Pool() as p: 
        pass 

    for person in entries:
        
        prog+=1 
        printProgressBar(prog, tot, prefix = 'Progress:', suffix = 'Complete', length = 50) 
        
        try: 
            data = readJustUrl(person)
            id = data["username"]
            wiki = data["wiki"]
            links +=1 
            allLinks[id] = {"wikiLink": wiki }

        except Exception as e: 
            noLinks +=1
            continue 

    error = round(noLinks/links, 2) 
    correct = (1-error)*100


    print(f"Percentage of Links we have: {correct}%")

    with open('wikis.json', 'w', encoding='utf-8') as f:
        json.dump(allLinks, f, ensure_ascii=False, indent=4)

    f.close()

   
def getBirthNames(): 
    import json 
    allLinks = {}
    noLinks = 0 
    links = 0 

    tot = len(entries)
    prog = 0 

    printProgressBar(0, tot, prefix = 'Progress:', suffix = 'Complete', length = 50)


    with Pool() as p: 
        pass 

    for person in entries:
        
        prog+=1 
        printProgressBar(prog, tot, prefix = 'Progress:', suffix = 'Complete', length = 50) 
        
        try: 
            data = readJustBirthname(person)
            id = data["username"]
            try: 
                birth_name = data["birthName"]
            except Exception as e: 
                birth_name = data["name"]
            name = data["name"]
            links +=1 
            allLinks[id] = {"birthName": birth_name, "name"  : name}

        except Exception as e:
            print(f"Error in {id} is {e}")
            noLinks +=1
            continue 

    error = round(noLinks/links, 2) 
    correct = (1-error)*100


    print(f"Percentage of Links we have: {correct}%")

    with open('birthNames.json', 'w', encoding='utf-8') as f:
        json.dump(allLinks, f, ensure_ascii=False, indent=4)

    f.close()

def getSingleURL(wiki): 

    try:

        wikilink = wiki
        paths = wikilink.split('/')
        title = paths[-1]
        url = return_image(title)
        global data 
        data[wiki] = url 
        return url 
    except Exception as e: 
        global errs 
        errs = errs + 1
        
        data[wiki] = None 
        return None 

#Reads json file to get profile pic from wikipedia links

def main3(): #56% of data has a wikilink 
    import json 
    import tqdm

    global data 

    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    warnings.filterwarnings('ignore', category=Warning, module='bs4')

    try:  
        wikis = readJson('wikis.json')

        tot = len(wikis) 
        prog = 0 

        

# puts all of the wiki links and url images in an array 
        wikiLinksArray = []
        urlImagesArray = []

        #printProgressBar(0, tot, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for username, profileData in wikis.items():

            # Adds all of the wiki links to a single array 
            wikiLinksArray.append(profileData["wikiLink"])

        
        pool = Pool(75)

        for _ in tqdm.tqdm(pool.imap(getSingleURL, wikiLinksArray), total=len(wikiLinksArray)):
            pass

        #data = dict(zip(wikiLinksArray, urlImagesArray))



        
        #write to json file 

        with open('urls.json', 'w', encoding='utf-8') as j:
            json.dump(data, j, ensure_ascii=False, indent=4)

        j.close()



        # process is infinished 
            



        # Multiprocessing 


        global errs 

        errPercentage = errs/tot 

        correct = (1-errPercentage)*100

        correct = round(correct, 2)

        totProf = round(0.56*correct, 2)

        print(f"The percentage of profiles we have with a profile link is {correct}% so in total we have  {totProf}% profile pictures. ")
        
        with open('profile_url_links.json', 'w', encoding='utf-8') as f:
            json.dump(wikis, f, ensure_ascii=False, indent=4)

        f.close()
    
    except Exception as error: 
        print(f"Some error {error} ")
        print("the error was " + str(error) )





def main():
   
    non_scientists = get_non_scientists()
    scientists = get_scientists()
    print(f'Found {len(non_scientists)} non scientists')
    print(f'Found {len(scientists)} scientists')
 



def main2():
    import time
    import json
    import uuid
    start_time = time.time()
    err = 0
    num_disagreements = 0 
    approvedRisings = 0 

    total = len(entries)

    
    

    print(f"We have {total} people in our database")
    iteration = 0 

    printProgressBar(0, total, prefix = 'Progress:', suffix = 'Complete', length = 50)

    for person in entries:
        iteration += 1
        try:
            printProgressBar(iteration, total,  prefix = 'Progress:', suffix = 'Complete', length = 50)
            p = readOne(person)

            try:
                p.createNatal()
            except Exception as e: 
                continue

            if p is not None: 
            
                uid = str(uuid.uuid1())

                jsonData[uid] = p.celebDict()
                natalData[uid] = p.natal()

                users.append(p)

                #Checks if rising signs match 
                if p.known_time: 
                    if p.risingFromCelebDate not in p.asc.sign.lower(): 
                        disagreements.append(p)
                        num_disagreements += 1
                        #print(f"{p.name} has a disagreement. Astrobank says {p.risingFromCelebDate} but he's actually a {p.asc.sign}")
                    else:
                        #print(f"{p.name} has no disagreement")
                        approvedRisings += 1 
        except ValueError as error:
            err = err+1
            #print(f"Error #{err} {error}")
            errors.append(err)
            continue

    print("It took: --- %s seconds ---" % (time.time() - start_time))
    print(f"We have {len(users)} users in our database and {err} bad data")
    error_percentage = round((float(num_disagreements/(approvedRisings+num_disagreements)) * 100), 2)
    print(f"The error percentage for our rising signs are:  {error_percentage}%")

    start = time.time() 

    print("Beginning to write to json")

    with open('celebBirthData.json', 'w', encoding='utf-8') as f:
        json.dump(jsonData, f, ensure_ascii=False, indent=4)

    with open('celebNatalData.json', 'w', encoding='utf-8') as j:
        json.dump(natalData, j, ensure_ascii=False, indent=4)

    f.close()
    j.close()

    print("It took: --- %s seconds ---" % (time.time() - start))
    

def importCelebritiesToFirestore():
    from datetime import datetime 
    import time 
    

    data = readJson(celebNatalData)
    iteration = 0 

    tot = len(data)

    start_time = time.time()


    printProgressBar(0, tot, prefix = 'Progress:', suffix = 'Complete', length = 50)

    for id, person in data.items():

        printProgressBar(iteration, tot,  prefix = 'Progress:', suffix = 'Complete', length = 50)


        username = person['username'].lower()
        userData = person

        stamp = userData['birthday']['timestamp'] 

        #changes the seconds since 1970 to datetime object
        userData['birthday']['timestamp'] = datetime.utcfromtimestamp(stamp)

        #Sets the id in the database 
        db.collection(f'notable_usernames_not_on_here').document(username).set({'userId': id, 'username': username, 'isNotable': True})

        
        #Sets the user data in the database
        db.collection(f'notables_not_on_here').document(id).set(userData)
        
        iteration += 1

    print("It took: --- %s seconds ---" % (time.time() - start_time))



def getIdByUsername(username):

    try: 
        id = db.collection(f'notable_usernames_not_on_here').document(username.lower()).get().to_dict()["userId"]
        return id 
    except Exception as e: 
        #print(f"Failed to get id {username} because {e}")
        return None 
        



def linkFromWiki(wiki): 
    try:
        wikilink = wiki
        paths = wikilink.split('/')
        title = paths[-1]

        profile_image = return_image(title)
        return profile_image
    except Exception as e:
        profile_image = None
        return None 
    
#inserts 'wiki' between a link to correct the url link 
def correctWikiLink(wiki): 
    try:
        wikilink = wiki
        paths = wikilink.split('/')
        title = paths[-1]

        url = ['https:', '', 'en.wikipedia.org', 'wiki', title]
        return '/'.join(url)
    except Exception as e:
        profile_image = None
        return None 

def setUrlToUsername(username, wikilink):

    print(f"Setting  {username} to {wikilink}")

    id = getIdByUsername(username)

    

    if id is not None:

        wiki = wikilink

        link = linkFromWiki(wiki) 

        if link is not None: 
             
            print(f"Setting... {username.lower()} to {link}")
            db.collection(f'notable_usernames_not_on_here').document(username.lower()).update({'profile_image_url': link})
            db.collection(f'notables_not_on_here').document(id).update({'profile_image_url': link})
            return (username, link)
        
    else: 
        return None
        pass 
    

def setWikiUrlToUsername(username, wikilink):

    print(f"Setting  {username} to {wikilink}")

    id = getIdByUsername(username)

    

    if id is not None:

        wiki = wikilink

        link = correctWikiLink(wiki) 

        if link is not None: 
             
            print(f"Setting... {username.lower()} to {link}")
            db.collection(f'notable_usernames_not_on_here').document(username.lower()).update({'wikipedia_link': link})
            db.collection(f'notables_not_on_here').document(id).update({'wikipedia_link': link})
            return (username, link)
        
    else: 
        return None
        pass 
    
 #tries to find the relationships the user had given their name and birthname
def setRelationships(username, name, birthname):
    from localdataset.scraping import getRelationships
    url = 'https://www.whosdatedwho.com/dating/'

    
    #returns an array of string elements split by a space
    names = name.split(' ') # Barack Obama --> [Barack, Obama]

    if birthname == None: 
        birthname = name 

    birthnames = birthname.split(' ')   # Michael B. Jordan --> [Michael, B., Jordan]

    

    #if any of the names in the array have a period, we need to remove it 
    for i in range(len(names)):
        if '.' in names[i]:
            names[i] = names[i].replace('.', '')

    # we do the name for the birthnames 
    for i in range(len(birthnames)):
        if '.' in birthnames[i]:
            birthnames[i] = birthnames[i].replace('.', '')
    
    name1 = '-'.join(names)
    try: 
        name2 = '-'.join([names[0], names[-1]])
    except: 
        name2 = name1
    birthname1 = '-'.join(birthnames)
    try: 
        birthname2 = '-'.join([birthnames[0], birthnames[-1]])
    except: 
        birthname2 = birthname1

    url1 = url + name1
    url2 = url + name2
    url3 = url + birthname1
    url4 = url + birthname2

    # try to get the relationships from url1 
    rel = getRelationships(url1)
    if rel is not None:
        data = {'username': username, 'relationships': rel, 'partnerAURL': url1}
        findRelationships(data)
        return {'username': username, 'relationships': rel}
    # try to get the relationships from url2
    rel = getRelationships(url2)
    if rel is not None:
        data = {'username': username, 'relationships': rel, 'partnerAURL': url2}
        findRelationships(data)
        return  {'username': username, 'relationships': rel}
    
    # try to get the relationships from url3
    rel = getRelationships(url3)
    if rel is not None:
        data = {'username': username, 'relationships': rel, 'partnerAURL': url3}
        findRelationships(data)
        return  {'username': username, 'relationships': rel}

    # try to get the relationships from url4
    rel = getRelationships(url4)
    if rel is not None:
        data = {'username': username, 'relationships': rel, 'partnerAURL': url4}
        findRelationships(data)
        return  {'username': username, 'relationships': rel}

    data = {'username': username, 'relationships': None, 'partnerAURL': None}
    findRelationships(data)
    return {'username': username, 'relationships': None}




 # given the relationships a username has, we try to find other users in our database that match the relationships of that user
def findRelationships(data): 
    import uuid
   
    username = data['username']

    if data['relationships'] == None: 
        return None 

    # Create tree in database 
    # notable_relationships (collection)
    #  - drake (coll)
    #       - relationships
    #             - username 
    #                       - relationship data 
    for rel in data['relationships']:
        name = rel['name'] 
        otherPerson = getUsernameByName(name)
        if otherPerson is not None: 
            rel["partnerAUsername"] = username
            rel["partnerBUsername"] = otherPerson
            rel["partnerAURL"] = data['partnerAURL']

            try: 
                rel["partnerBURL"] = data['url']
            except: 
                rel["partnerBURL"] = None
            #cleaning some of the omitted data
            if rel["began"] == '': 
                rel["began"] = None

            if rel["ended"] == '': 
                rel["ended"] = None

            if rel["length"] == '-': 
                rel["length"] = None


            print(f"\n\n\nSetting {rel}")
            db.collection(f'notable_relationships').document(str(uuid.uuid1())).set(rel)
            #print(f"Added {username} to {rel}")
        else:
            #TODO add to database of people who are not on here
            #if they are not in OUR database... add scrap for their data and add anyway 
            #incomplete data 
            # - incomplete notable relationships 
            #       - document 
            #             - link for partnerA
            #             - link for partnerB
            rel["partnerAUsername"] = username
            rel["partnerBUsername"] = None
            rel["partnerAURL"] = data['partnerAURL']
            try: 
                rel["partnerBURL"] = data['url']
            except: 
                rel["partnerBURL"] = None
            #cleaning some of the omitted data
            if rel["began"] == '': 
                rel["began"] = None

            if rel["ended"] == '': 
                rel["ended"] = None

            if rel["length"] == '-': 
                rel["length"] = None

            print(f"\n\n\nSETTING INCOMPLETE DATA: {rel}")
            db.collection(f'incomplete_data_notable_relationships').document(str(uuid.uuid1())).set(rel)




    pass 
    
def getUsernameByName(name): 
    #loops through all birthnames to find a username that matches the name 
    from difflib import SequenceMatcher
    for key, value in birthNames.items():
        nameToCheck = value["name"] 
        birthName = value["birthName"]

        if birthName == None: 
            birthName = nameToCheck

        #check for exact match first 
        if nameToCheck.lower() == name.lower() or birthName.lower() == name.lower(): 
            return key

        #check for partial match
        if SequenceMatcher(None, nameToCheck.lower(), name).ratio() > 0.75:
            return key
        
        if SequenceMatcher(None, birthName.lower(), name).ratio() > 0.75:
            return key
        

    return None
    

    


# Loops through eacn username we have and finds the profile url of the celeb and writes to username database and info
def main5():
    import tqdm 
    import time
   

    stuff = readJson('wikis.json')

    start_time = time.time()
    
    usernamesAndWikis = []

    for key, value in stuff.items(): 

        data = (key, value["wikiLink"])

        usernamesAndWikis.append(data)

    print(f"Total is .. {len(usernamesAndWikis)}")

    


    pool = Pool(75)

    
    for result in tqdm.tqdm(pool.starmap(setUrlToUsername, usernamesAndWikis), total=len(usernamesAndWikis)):
        pass 

    
    print("It took: --- %s seconds ---" % (time.time() - start_time))
    print("I have finished.")


# loops through each username and gets the wiki link and writes to the database
def main6():
    import tqdm 
    import time
   

    stuff = readJson('wikis.json')

    start_time = time.time()
    
    usernamesAndWikis = []

    for key, value in stuff.items():

       

        
        data = (key, value["wikiLink"])

        usernamesAndWikis.append(data)

    print(f"Total is .. {len(usernamesAndWikis)}")

    


    pool = Pool(75)

    
    for result in tqdm.tqdm(pool.starmap(setWikiUrlToUsername, usernamesAndWikis), total=len(usernamesAndWikis)):
        pass 

    
    print("It took: --- %s seconds ---" % (time.time() - start_time))
    print("I have finished.")


    


    

    





#Returns a dictionary from a json file
def readJson(file):
     
    with open(file, 'r') as f:
        return json.load(f)
    f.close()


birthNames = readJson('birthNames.json')


def main7(): 
    import tqdm 
    import time
   


    

    start_time = time.time()
    
    usernamesAndBirthNames = []

    for key, value in birthNames.items(): 


        data = (key, value["name"], value["birthName"])
        

        usernamesAndBirthNames.append(data)

    print(f"Total number of items to collect is .. {len(usernamesAndBirthNames)}")

    


    pool = Pool(75)

    
    for result in tqdm.tqdm(pool.starmap(setRelationships, usernamesAndBirthNames), total=len(usernamesAndBirthNames)):
        pass 

    
    print("It took: --- %s seconds ---" % (time.time() - start_time))
    print("I have finished.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main3()


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



def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()




def reindexDataByUsernames():
    users = readJson('celebBirthData.json')

def firebaseToDatabase():

    from datetime import datetime 
    import csv


    dataForCSV = []

    usersbyusername = readJson('data_by_usernames.json')

    celeb_relationships = readJson('celeb_relationships.json') # an array of celeb relationships from database

    for dic in celeb_relationships: 
        for username, data in dic.items(): 

            try: 

                client = data['partnerAUsername']


                clientLatitude = usersbyusername[client]["hometown"]["latitude"]
                clientLongitude = usersbyusername[client]["hometown"]["longitude"]
                clientTimestamp =  usersbyusername[client]["birthday"]["timestamp"]
                clientSex =  usersbyusername[client]["sex"]

                clientObject = User(do_not_fetch=True, hometown=Location(latitude=clientLatitude, longitude=clientLongitude), birthday=datetime.utcfromtimestamp(clientTimestamp), known_time=True, sex=clientSex)
                partner = data['partnerBUsername']

                partnerLatitude = usersbyusername[partner]["hometown"]["latitude"]
                partnerLongitude = usersbyusername[partner]["hometown"]["longitude"]
                partnerTimestamp = usersbyusername[partner]["birthday"]["timestamp"]
                partnerSex = usersbyusername[partner]["sex"]


                partnerObject = User(do_not_fetch=True, hometown=Location(latitude=partnerLatitude, longitude=partnerLongitude), birthday=datetime.utcfromtimestamp(partnerTimestamp), known_time=True, sex=partnerSex)

                rel_type = data['relationship_type']


                length = lengthStringToNumber(data['length'])

                if rel_type == 'Marriage': 
                    if length == None: 
                        somewhat_successful_marriage = None

                    if ended == 'present': 
                        somewhat_successful_marriage = None
                    
                    else: 
                        if length >= 240: 
                            somewhat_successful_marriage = True  #greater than 20 years 
                        if length <= 120:
                            somewhat_successful_marriage = False   # less than 10 years 
                        else: 
                            somewhat_successful_marriage = None 
                else: 
                    somewhat_successful_marriage = None 

                
               
                
                partnerAURL = data['partnerAURL']
                partnerBURL = data['partnerBURL']
                isRumor = data['is_rumor']
                began = data['began']
                ended = data['ended']

                sexuality = 'other'

                if clientObject.sex == 'male' and partnerObject.sex == 'female': 
                    syn = clientObject.synastry(partnerObject)
                    sexuality = 'mf'
                elif clientObject.sex == 'female' and partnerObject.sex == 'male': 
                    syn = partnerObject.synastry(clientObject)
                    sexuality = 'mf'
                elif partnerObject.sex == 'male' and clientObject.sex == 'male':
                    syn = clientObject.synastry(partnerObject)
                    sexuality = 'mm'
                elif partnerObject.sex == 'female' and clientObject.sex == 'female':
                    syn = clientObject.synastry(partnerObject)
                    sexuality = 'ff'
                else: 
                    syn = clientObject.synastry(partnerObject)

               

                feat = syn.getFeaturesForSynastry()

                try:
                    for key in list(feat.keys()): 
                        if 'Asc' in key or 'MC' in key or 'IC' in key or 'Desc' in key: 
                            del(feat[key])
                except: 
                    print("problem in keys")
                    pass 

                try: 
                    del(feat['MC-Asc_aspectBySign'])
                except:
                    pass 

                try: 
                    del(feat['MC-Desc_aspectBySign'])
                except:
                    pass

                try: 
                    del(feat['MC-Desc_orb'])
                except:
                    pass

                try: 
                    del(feat['MC-Asc_aspect'])
                except:
                    pass

                try: 
                    del(feat['MC-Asc_orb'])
                except:
                    pass

                try: 
                    del(feat['MC-Desc_aspect'])
                except: 
                    pass 

                try: 
                    del(feat['MC-MC_aspect'])
                except: 
                    pass 

                try: 
                    del(feat['MC-IC_aspect'])
                except: 
                    pass 

                try: 
                    del(feat['MC-IC_aspectBySign'])
                except: 
                    pass 

                try: 
                    del(feat['MC-MC_aspectBySign'])
                except: 
                    pass 

                try: 
                    del(feat['MC-IC_orb'])
                except: 
                    pass 

                try: 
                    del(feat['MC-MC_orb'])
                except: 
                    pass 

                try: 
                    del(feat['MC-MC_aspect'])
                except: 
                    pass 

                row = {

                    'PersonA': client, 
                    'PersonALatitude': clientLatitude, 
                    'PersonALongitude' : clientLongitude, 
                    'PersonABirthday': clientTimestamp, 
                    'PersonAURL': partnerAURL, 

                    'PersonB': partner, 
                    'PersonBLatitude': partnerLatitude, 
                    'PersonBLongitude' : partnerLongitude, 
                    'PersonBBirthday': partnerTimestamp, 
                    'PersonBURL': partnerBURL, 

                    'relationshipType': rel_type, 
                    'length': length, 
                    'began': began, 
                    'ended': ended, 
                    'isRumor': isRumor,

                    'relationship_sexuality': sexuality,  # mf, ff, o , mm 
                    'somewhat_successful_marriage': somewhat_successful_marriage

                }

                row.update(feat)

                dataForCSV.append(row)

                #if length != None: 
                    #dataForCSV.append(row)

            except Exception as e: 
                print(f"The error is {e}")
        
    y = dataForCSV[0]
   
    with open('relationship_sample_database_1.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = list(y.keys()))
        writer.writeheader()
        writer.writerows(dataForCSV)

    csvfile.close()

            
    
    return dataForCSV


     
def lengthStringToNumber(length): 
    if length == None: 
        return None 
    if '<' in length: 
        return 0.5 
    if 'month' in length or 'months' in length: 
        return float(''.join(filter(str.isdigit, length)))
    elif 'year' in length or 'years' in length: 
         years =  float(''.join(filter(str.isdigit, length)))
         return years*12 
    else: 
        return None