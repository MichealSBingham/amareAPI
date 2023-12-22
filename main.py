from flask import jsonify
import traceback
from secret import api_keys
from google.cloud import firestore
from database.user import db, User
from google.cloud.firestore_v1 import Transaction
from json import dumps
from flask import make_response
from Messaging.streamBackend import *
from google.cloud import pubsub_v1
import base64
import subprocess
import json





def publish_to_pubsub(topic, data):
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path('findamare', topic)
        message = json.dumps(data).encode('utf-8')

        # Publish the message
        future = publisher.publish(topic_path, data=message)
        future.result()  # Wait for the message to be published
        print(f"Message published to topic {topic}")

    except Exception as e:
        print(f"Error publishing to Pub/Sub: {e}")




# Example data


# Example usage

#publish_to_pubsub('update_aspects', data)



def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response


## Admin Functions ...

# Get's the natal chart of a user by user id.
'''  


HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
        
 Deployment:
     gcloud functions deploy user \
--runtime python37 --trigger-http  --security-level=secure-always --allow-unauthenticated

Delete:
gcloud functions delete func_name

Get url to end point
gcloud functions describe func_name


Returns the user data. No natal chart or anything though.  

- Request Parameters: 
     - SECRET (String) : secret id used to authenticate for the admin api 
     - id:   (String)   user id of user requesting 
     
- Returns 
     - success (Bool) : true or false of whether the response was successful. This will be in any request 
     - error: (JSON) 
                - code (INT)                :       Error code , (400 Bad request)
                - description (String)      :       Description of the error 

'''

def user(request):

    request_json = request.get_json(silent=True)
    request_args = request.args



# Ensuring proper authorization
    if request_json and 'secret' in request_json:
        secret = request_json['secret']
    elif request_args and 'secret' in request_args:
        secret = request_args['secret']
    else:
        return jsonify(success=False,
                error={
                    'code' : 400,
                    'description': "BAD REQUEST. Failed to authenticate, no secret key provided."}
                )

    if secret == api_keys.SECRET:

        if request_json and 'id' in request_json:
            id = request_json['id']
        elif request_args and 'id' in request_args:
            id = request_args['id']
        else:
            return jsonify(success=False,
                           error={
                               'code': 400,
                               'description': "BAD REQUEST. Did not provide user id."}
                           )

        try:
            user = User(id=id)

            if not user.exists:

                return jsonify(success=False,
                               error={
                                   'code': 404,
                                   'description': "USER NOT FOUND. Could not find user with id " + id + ", or the user has no information saved."
                                   }
                               )


            return jsonify(success=True,
                           user=user.dict())

        except Exception as e:


            return jsonify(success=False,
                           error={
                               'code': 404,
                               'description': "USER NOT FOUND. Could not find user with id " + id + ".",
                               'why': str(e),
                               'trace': traceback.format_exc()}
                           )



    else:
        return jsonify(success=False,
                       error={
                           'code': 401,
                           'description': "UNAUTHORIZED. Failed to authenticate, invalid secret key."},
                       secret_entered=secret
                       )



"""

Returns the Celebrity Soulmate of the user  

- Request Parameters: 
     - name (String) : The name of the user 
     - gender:   (String)   male, female, or other 
     - orientation: (String) male, female, or other
     - latitude: (Number) latitude of birth location
     - longitude: (Number) longitude of birth location 
     - birthday: (Timestamp) Birthday of the user in UTC. This should be the timestamp: secondsSince(1970)

 Deployment:
     gcloud functions deploy celebritySoulmate \
--runtime python37 --trigger-http  --security-level=secure-always --allow-unauthenticated

Get Url to endpoing: 
gcloud functions describe celebritySoulmate


"""
def celebritySoulmate(request): 

    from database.user import User
    from database.Location import Location
    from datetime import datetime
    import random 
    import flask 

    request_json = request.get_json(silent=True)
    request_args = request.args

    gender = name =  orientation = latitude = longitude =  birthday = None 
    knownTime = True 


    if request_json and 'name' in request_json:
            name = request_json['name']
    else: 
        resp = {"success": False, "error": {"code": 400, "description": "Invalid Parameters. Please provide a name."}}
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp

    if request_json and 'gender' in request_json:
            gender = request_json['gender']

    else: 
        resp = {"success": False, "error": {"code": 400, "description": "Invalid Parameters. Please provide a gender."}}
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp


    if request_json and 'orientation' in request_json:
            orientation = request_json['orientation']

    else: 
        resp = {"success": False, "error": {"code": 400, "description": "Invalid Parameters. Please provide an orientation."}}
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp

    if request_json and 'latitude' in request_json:
            latitude = request_json['latitude']
    
    else: 
        resp = {"success": False, "error": {"code": 400, "description": "Invalid Parameters. Please provide a latitude."}}
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp

    if request_json and 'longitude' in request_json:
            longitude = request_json['longitude']
    else: 
        

        resp = {"success": False, "error": {"code": 400, "description": "Invalid Parameters. Please provide a longitude."}}
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp

    if request_json and 'birthday' in request_json:
            birthday = request_json['birthday']
    else: 
        resp = {"success": False, "error": {"code": 400, "description": "Invalid Parameters. Please provide a birthday."}}

        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp

    if request_json and 'knownTime' in request_json: 
        knownTime =  request_json['knownTime']

    
    try: 
        birthday = float(birthday)
        latitude = float(latitude)
        longitude = float(longitude) 
    except Exception as e: 
        resp =  jsonify(success=False,
                       error={
                           'code': 405,
                           'description': f"Please enter numbers as strings {e.message}"}
                       )
        #resp = flask.Response(response)
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp
    
    #TODO: FIX THIS!
    try: #IMPORTANT! 
        date = datetime.fromtimestamp(float(birthday)) # For some reason, this is not when you run on system. 
                                # on sysstem, you MUST specifiy utcfromtimestamp but on server this seems to work. 
    except Exception as e: 
        resp =  jsonify(success=False,
                       error={
                           'code': 400,
                           'description': f"An invalid birthday was given. {e.message}"}
        )
        #resp = flask.Response(response)
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp
        
    try: 
        loc = Location(latitude=float(latitude), longitude=float(longitude))
    except Exception as e: 
        resp =  jsonify(success=False,
                       error={
                           'code': 401,
                           'description': f"An invalid location was given. {e.message}"}
                       ) 
        #resp = flask.Response(response)
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp

    
    try: 
        user = User(do_not_fetch=True, name=name, birthday=date, known_time=True, hometown=loc)
    except Exception as e: 
        resp =  jsonify(success=False,
                       error={
                           'code': 500,
                           'description': f"Something went wrong trying to draw the user's natal chart. {e.message}"}
                       ) 
        #resp = flask.Response(response)
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp
            
    try: 
        natal_response = user.natal()
        #natal_response["success"] = True
    except Exception as e: 
        resp = jsonify(success=False,
                       error={
                           'code': 409,
                           'description': f"Something went wrong. {e.message}"}
                       ) 

        #resp = flask.Response(response)
        resp = jsonify(**resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")

        return resp


    # Getting the celebrity soulmate 

    celeb = user.celebritySoulmate()
    celeb.residence = None 
    response = celeb.dict()

    response["natal_chart"] = natal_response

    response["sex"] = random.randint(0,100) 
    response["chemistry"] = random.randint(0,100) 
    response["love"] = random.randint(0,100) 
    response["id"] = celeb.id 
    response["location"] = {"latitude": latitude, "longitude": longitude}
    response["timestamp"] = birthday
    response["oneLiner"] = "You two have something very beautiful."

    response = {k: v for k, v in response.items() if
                             v is not None and v != '' and (v != {}) and (v != [])}


    resp = jsonify(**response)
    resp.headers.set('Access-Control-Allow-Origin','*')
    resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")


    return resp #jsonify(**response)
     

"""
Returns the natal chart of the user

Provide ID OR (birthday and location) 
 - Parameters: 
           - id : String (user id of the user) [optional if you provide bday and location] 
           - secret: String ( secret key for auth) 
           - birthday: String 'YYYY/MM/DD'  ('1999/07/21')  [optional if you have id] 
           - birth_time: String '19:52' MUST BE IN UTC TIME AT THE MOMENT. [optional]
           - latitude: Int [optional if you provide id or location]
           - longitude: int ^ 
           - location: String (Natural language location to search... i.e. 'One world trade center', 'NYC', 'Atlanta, GA') etc .
           - natal_orb: Int Orb to use for natal charts for planetary signs to determine cusps (NOT for aspect orbs) 
"""
def natal(request):
    from astrology.NatalChart import planetToDict

    #Pulling from database
    providedId = False

    #Creating a chart from scratch with bday and time
    providedBirthday = False
    providedTime = False
    providedCoordinates = False
    providedLocationToSearch = False

    request_json = request.get_json(silent=True)
    request_args = request.args

    # Ensuring proper authorization
    if request_json and 'secret' in request_json:
        secret = request_json['secret']
    elif request_args and 'secret' in request_args:
        secret = request_args['secret']
    else:
        return jsonify(success=False,
                       error={
                           'code': 400,
                           'description': "BAD REQUEST. Failed to authenticate, no secret key provided."}
                       )

    if request_json and 'birthday' in request_json:         # (String) "YYYY/MM/DD" Ex; "1999/07/21"
        birthday = request_json['birthday']
        providedBirthday = True
    elif request_args and 'birthday' in request_args:
        birthday = request_args['birthday']
        providedBirthday = True
    else:
        providedBirthday = False

    if request_json and 'birth_time' in request_json:
        time = request_json['birth_time']
        providedTime = True
    elif request_args and 'birth_time' in request_args:
        time = request_args['birth_time']
        providedTime = True
    else:
        time = "12:00"
        providedTime = False

    if request_json and 'latitude' in request_json:  # (String) "YYYY/MM/DD" Ex; "1999/07/21"
        latitude = request_json['latitude']
        providedLatitude = True
    elif request_args and 'latitude' in request_args:
        latitude = request_args['latitude']
        providedLatitude = True
    else:
        providedLatitude = False

    if request_json and 'longitude' in request_json:  # (String) "YYYY/MM/DD" Ex; "1999/07/21"
        longitude = request_json['longitude']
        providedLongitude = True
    elif request_args and 'longitude' in request_args:
        longitude = request_args['longitude']
        providedLongitude = True
    else:
        providedLongitude = False

    if providedLatitude and providedLongitude:
        providedCoordinates = True
    else:
        providedCoordinates = False



    if request_json and 'location' in request_json:  # (String) "YYYY/MM/DD" Ex; "1999/07/21"
        location = request_json['location']
        providedLocationToSearch = True
    elif request_args and 'location' in request_args:
        location = request_args['location']
        providedLocationToSearch = True
    else:
        providedLocationToSearch = False


    if request_json and 'natal_orb' in request_json:  # (String) "YYYY/MM/DD" Ex; "1999/07/21"
        natal_orb = int(request_json['natal_orb'])
    elif request_args and 'natal_orb' in request_args:
        natal_orb = int(request_args['natal_orb'])
    else:
        natal_orb = 3 # default orb





            # If authorized
    if secret == api_keys.SECRET:


        if request_json and 'id' in request_json:
            id = request_json['id']
            providedId = True
        elif request_args and 'id' in request_args:
            id = request_args['id']
            providedId = True

        else:
            pass
            """"
            return jsonify(success=False,
                           error={
                               'code': 400,
                               'description': "BAD REQUEST. Did not provide user id."}
                           )
"""

        try:

            if providedId:


                try:
                    user = User(id=id)

                    if not user.exists:   #user does not exist
                        return jsonify(success=False,
                                       error={
                                           'code': 404,
                                           'description': "USER NOT FOUND. User with id " + id + " does not exist."}
                                       )

                    chart = user.natal(set_orb=natal_orb)

                    #add success to response
                    chart["success"] = True
                    return jsonify(**chart)


                except Exception as e:  #could not get the planets
                    return jsonify(success=False,
                           error={
                               'code': 500,
                               'description': "USER DATA INCOMPLETE. Could not get chart data from user with id " + id + ".",
                               'why': str(e),
                               'trace': traceback.format_exc()}
                           )


            else:
                from flatlib.datetime import Datetime

                if providedBirthday and (providedCoordinates or providedLocationToSearch):
                    from database.Location import Location

                    if providedCoordinates:
                        try:
                            date = Datetime(birthday, time)
                            user = User(birthday=date, hometown=Location(latitude=latitude, longitude=longitude), known_time=providedTime)

                            natal_response = user.natal(set_orb=natal_orb)
                            natal_response["success"] = True
                            return jsonify(**natal_response)


                        except Exception as e:
                            return jsonify(success=False,
                                    error={
                                        'code': 412,
                                        'description': "INVALID PARAMETERS. Not able to draw natal chart with given date and location.",
                                        'why': str(e),
                                        'trace': traceback.format_exc()}
                                    )

                    if providedLocationToSearch:


                        location = Location(search=location)


                        if location.latitude is None or location.longitude is None:  #// COuld not find the location the user entered
                            return jsonify(success=False,
                                           error={
                                               'code': 404,
                                               'description': "LOCATION NOT FOUND. Please enter a new search for the location or use coordinates."}
                                           )
                        else:

                            try:
                                date = Datetime(birthday, time)
                                user = User(birthday=date, hometown=location, known_time=providedTime)
                                natal_response = user.natal(set_orb=natal_orb)


                                natal_response["success"] = True
                                return jsonify(**natal_response)



                            except Exception as e:  #// Could not draw natal chart due to inputted date and location
                                 return jsonify(success=False,
                                            error={
                                                    'code': 412,
                                                    'description': "INVALID PARAMETERS. Not able to draw natal chart with given date and location.",
                                                     'why': str(e),
                                                      'trace': traceback.format_exc()}
                           )


                else:     #Did not include proper parameters
                    return jsonify(success=False,
                                   error={
                                       'code': 412,
                                       'description': "MISSING PARAMETERS. You must either specify a user id or include a birthday and birth city or coordinates to the city."}
                                   )


        except Exception as e:

            return jsonify(success=False,
                           error={
                               'code': 404,
                               'description': "USER NOT FOUND. Could not find user with id " + id + ".",
                               'why': str(e),
                               'trace': traceback.format_exc()}
                           )



    else:
        return jsonify(success=False,
                       error={
                           'code': 401,
                           'description': "UNAUTHORIZED. Failed to authenticate, invalid secret key."},
                       secret_entered=secret
                       )








def listen_for_new_user(data, context):
    """"
  # Run this to deploy. Reads
      gcloud functions deploy listen_for_new_user \
    --runtime python38 \
    --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
    --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}" \
    --timeout=540s
      """

    from analytics.app_data import new_user
    from database.user import db
    from database.Location import Location
    import iso8601
    import time
    from prompts.astrology_traits_generator import DashaChatBot

    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])

    affected_doc = db.collection(collection_path).document(document_path)
    id = document_path

    dataHere = data["value"]['fields']
    print("Data that's already here after new user added is: ")
    print(dataHere)

    if 'hometown' in dataHere and 'birthday' in dataHere:

        try:

            lat = dataHere['hometown']['mapValue']['fields']['latitude']['doubleValue']
            lon = dataHere['hometown']['mapValue']['fields']['longitude']['doubleValue']
            location = Location(latitude=lat, longitude=lon)


            bday = dataHere['birthday']['mapValue']['fields']['timestamp']['timestampValue']
            date = iso8601.parse_date(bday) #converts the timestamp String into a datetime object
            isNotable = dataHere['isNotable']['booleanValue']
            isReal = dataHere['isReal']['booleanValue']

            try:
                known_time = dataHere['known_time']['booleanValue']
            except:
                known_time = False

            user = User(id=id,
                        do_not_fetch=True,
                        hometown=location,
                        birthday=date,
                        known_time=known_time,
                        is_notable=isNotable,
                        isReal=isReal
                        )
            # Set it in database now
            user.set_natal_chart()
            new_user()
            time.sleep(100)
            DashaChatBot.createInitialThread(id)
            
        except Exception as error:
            print(f"This data does not exist in the database yet or some error:  {error}")

    else:  #Update analytics because this is probably a new user
        new_user()

""""
    #updated_attributes = data["updateMask"][
       # "fieldPaths"]  # returns list of attributes updated on commit in firebase  ex: ['hometown']
    user_data = data["value"]
    #old_user_data = data['oldValue']

    #print("The updated attributes are: ")
    #print(updated_attributes)

    print("The user data is ... value: ")
    print(user_data)

    print("the data in general is ... ")
    print(data)
    """




# THis function is a too long process and it is timing out.. seek alternative solution  because the indexes never write due to it timining out
def listen_for_new_natal_chart_and_write_indexes(data, context):
    """"
     # Run this to deploy. Reads
         gcloud functions deploy listen_for_new_natal_chart_and_write_indexes \
       --runtime python38 \
       --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
       --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}/public/natal_chart" \
       --timeout=540s

        """
    
    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path, document_path, user_id = path_parts[0], '/'.join(path_parts[1:]), path_parts[1]

    natal_chart_doc = db.collection(collection_path).document(document_path).get()
    natal_dict = natal_chart_doc.to_dict()

    user = User(id=user_id, skip_getting_natal=True)

    data = {
    "collection_path": collection_path,
    "document_path": document_path,
    "user_id": user_id
    }
    

    def update_aspects(user, natal_dict):
        aspects = natal_dict['aspects']
        for aspect in aspects:
            if aspect['type'] != 'NO_ASPECT':
                add_aspect_to_db(aspect, user)

    def add_aspect_to_db(aspect, user):
        aspect_data = {
            'profile_image_url': user.profile_image_url,
            'name_belongs_to': user.name,
            'isReal': user.isReal,
            **aspect  # Unpack aspect dictionary into aspect_data
        }

        # Add aspect to the database
        first, second = aspect['first'], aspect['second']
        db.collection(f'all_natal_aspects_for_all_users').document(first).collection(second).document('doc').collection(aspect['type']).document(user.id).set(aspect_data)
        #add_aspect_research_data(user, aspect, aspect_data)



    publish_to_pubsub('write_planet_interpretations_1', data)
    publish_to_pubsub('write_planet_interpretations_2', data)
    publish_to_pubsub('write_planet_interpretations_3', data)

    publish_to_pubsub('add_planet_placements', data)
    


    update_aspects(user, natal_dict)



def add_planet_placements(event, context): 

    """  Reads the user's planet placements and adds to the databse. 
    gcloud functions deploy add_planet_placements \
    --runtime python38 \
    --trigger-topic add_planet_placements
    """
    
   
    message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_data = json.loads(message)
    print(f"pubsub data is .. {pubsub_data}")

    # Access individual strings
    collection_path = pubsub_data['collection_path']
    document_path = pubsub_data['document_path']
    user_id = pubsub_data['user_id']

    natal_chart_doc = db.collection(collection_path).document(document_path).get()
    natal_dict = natal_chart_doc.to_dict()

    user = User(id=user_id, skip_getting_natal=True)
    def add_planet_placement_to_db(planet, user):

        common_data = {
            'is_on_cusp': planet['is_on_cusp'],
            'angle': planet['angle'],
            'is_retrograde': planet['is_retrograde'],
            'is_notable': user.is_notable,
            'house': planet.get('house'),
            'profile_image_url': user.profile_image_url,
            'name': user.name
        # Add user placement to the database
    
        }
        db.collection(f'all_users_placements').document(planet['name']).collection(planet['sign']).document(user.id).set(common_data)
    
    def update_planet_placements(user, natal_dict):
        planets = natal_dict['planets']
        for planet in planets:
            add_planet_placement_to_db(planet, user)
    update_planet_placements(user, natal_dict)


def write_planet_interpretations_1(event, context):

    """  Writes the first part of the planet interpretations to the database
    gcloud functions deploy write_planet_interpretations_1 \
    --runtime python38 \
    --trigger-topic write_planet_interpretations_1 \
    --timeout=540s
    """
    print("write_planet_interpretations_1")
    
    

    message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_data = json.loads(message)
    print(f"pubsub data is .. {pubsub_data}")

    # Access individual strings
    collection_path = pubsub_data['collection_path']
    document_path = pubsub_data['document_path']
    user_id = pubsub_data['user_id']

    natal_chart_doc = db.collection(collection_path).document(document_path).get()
    natal_dict = natal_chart_doc.to_dict()

    user = User(id=user_id, skip_getting_natal=True)
    def write_all_planet_interpretations():
        from prompts.astrology_traits_generator import PlacementInterpretationsGenerator
        reader = PlacementInterpretationsGenerator()
        gender = user.sex
        sortedPlanets = sorted(natal_dict['planets'], key=lambda x: x['angle'])
        first4planets = sortedPlanets[:4]
        for planet in first4planets:
            try:
                house_num = str(planet.get('house', ""))
                if house_num.isdigit():
                    house_num = "{}{}".format(house_num, 'th' if 4 <= int(house_num) % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(int(house_num) % 10, 'th'))
                interpretation = reader.interpret_placement(gender, planet['name'], planet['sign'], house_num)
                update_interpretation(user_id=user_id, planet=planet['name'], interpretation=interpretation)
            except Exception as e:
                print(f"Error interpreting planet {planet['name']}: {e}") 

    write_all_planet_interpretations() 

def write_planet_interpretations_2(event, context):

    """  Writes the first part of the planet interpretations to the database
    gcloud functions deploy write_planet_interpretations_2 \
    --runtime python38 \
    --trigger-topic write_planet_interpretations_2 \
    --timeout=540s
    """

    message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_data = json.loads(message)
    print(f"pubsub data is .. {pubsub_data}")

    # Access individual strings
    collection_path = pubsub_data['collection_path']
    document_path = pubsub_data['document_path']
    user_id = pubsub_data['user_id']

    natal_chart_doc = db.collection(collection_path).document(document_path).get()
    natal_dict = natal_chart_doc.to_dict()

    user = User(id=user_id, skip_getting_natal=True)
    def write_all_planet_interpretations():
        from prompts.astrology_traits_generator import PlacementInterpretationsGenerator
        reader = PlacementInterpretationsGenerator()
        gender = user.sex
        sortedPlanets = sorted(natal_dict['planets'], key=lambda x: x['angle'])
        mid4planets = sortedPlanets[3:7]
        for planet in mid4planets:
            try:
                house_num = str(planet.get('house', ""))
                if house_num.isdigit():
                    house_num = "{}{}".format(house_num, 'th' if 4 <= int(house_num) % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(int(house_num) % 10, 'th'))
                interpretation = reader.interpret_placement(gender, planet['name'], planet['sign'], house_num)
                update_interpretation(user_id=user_id, planet=planet['name'], interpretation=interpretation)
            except Exception as e:
                print(f"Error interpreting planet {planet['name']}: {e}") 

    write_all_planet_interpretations() 
     
def write_planet_interpretations_3(event, context):

    """  Writes the first part of the planet interpretations to the database
    gcloud functions deploy write_planet_interpretations_3 \
    --runtime python38 \
    --trigger-topic write_planet_interpretations_3 \
    --timeout=540s
    """

    
    message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_data = json.loads(message)
    print(f"pubsub data is .. {pubsub_data}")

    # Access individual strings
    collection_path = pubsub_data['collection_path']
    document_path = pubsub_data['document_path']
    user_id = pubsub_data['user_id']

    natal_chart_doc = db.collection(collection_path).document(document_path).get()
    natal_dict = natal_chart_doc.to_dict()

    user = User(id=user_id, skip_getting_natal=True)
    def write_all_planet_interpretations():
        from prompts.astrology_traits_generator import PlacementInterpretationsGenerator
        reader = PlacementInterpretationsGenerator()
        gender = user.sex
        sortedPlanets = sorted(natal_dict['planets'], key=lambda x: x['angle'])
        last4planets = sortedPlanets[-4:]
        for planet in last4planets:
            try:
                house_num = str(planet.get('house', ""))
                if house_num.isdigit():
                    house_num = "{}{}".format(house_num, 'th' if 4 <= int(house_num) % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(int(house_num) % 10, 'th'))
                interpretation = reader.interpret_placement(gender, planet['name'], planet['sign'], house_num)
                update_interpretation(user_id=user_id, planet=planet['name'], interpretation=interpretation)
            except Exception as e:
                print(f"Error interpreting planet {planet['name']}: {e}") 

    write_all_planet_interpretations() 
#Winked vs Winker in database --> winks / {winked} / peopleWhoWinked / {winker}
def listen_for_winks_DEPRECATED(data, context):
    """"
      # Run this to deploy. Reads
          gcloud functions deploy listen_for_winks \
        --runtime python37 \
        --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
        --trigger-resource "projects/findamare/databases/(default)/documents/winks/{winked}/people_who_winked/{winker}"
          """



    from database.user import db
    from database.notifications import PushNotifications
    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    print("The collection_path: %s" % collection_path)
    winked = path_parts[1]
    print("The winked: %s" % winked)

    #affected_doc = db.collection(collection_path).document(document_path)
    #print("The afected_doc: %s" % affected_doc)

    winker = path_parts[3] # Should be the winked , not the winker
    print("The winked: %s" % winked)


    trigger_resource = context.resource
    print('***Function triggered by change to: %s' % trigger_resource)

    # See if the it's a wink back (2 way wink)
    # Check if /winks/{winker}/people_who_winked/{winked} exists
    doc_ref = db.collection('winks').document(winker).collection('people_who_winked').document(winked)
    doc = doc_ref.get()
    if doc.exists:
        #Two way wink
        # Tell the 'winked' that 'winker' winked back
        PushNotifications.winked_back(winked, winker)
    else:
        # One way wink
        # One way wink: Send notification that someone winked at them
        PushNotifications.winked_at(winked, winker)



def write_aspect_interpretations(event, context):

    

    """  Writes the first part of the aspect interpretations to the database
    gcloud functions deploy write_aspect_interpretations \
    --runtime python38 \
    --trigger-topic write_aspect_interpretations_1 \
    --timeout=540s
    
    """

    message = base64.b64decode(event['data']).decode('utf-8')
    pubsub_data = json.loads(message)
    print(f"pubsub data is .. {pubsub_data}")

    collection_path = pubsub_data['collection_path']
    document_path = pubsub_data['document_path']
    user_id = pubsub_data['user_id']

    natal_chart_doc = db.collection(collection_path).document(document_path).get()
    natal_dict = natal_chart_doc.to_dict()

    def write_all_aspect_interpretations():
        from prompts.astrology_traits_generator import PlacementInterpretationsGenerator
        reader = PlacementInterpretationsGenerator()
        gender = user.sex
        aspects = natal_dict['aspects']
        for aspect in aspects:
            try:

                interpretation = reader.interpret_aspect(gender, aspect["first"], aspect["type"], aspect["second"], round(aspect["orb"]))
                update_aspect_interpretation(user_id=user_id, name=aspect['name'], interpretation=interpretation)
            except Exception as e:
                print(f"Error interpreting planet {aspect['name']}: {e}")  
    write_all_aspect_interpretations()

#I THINK this is OLD 
def listen_for_friend_requests(data, context):
    """"
          # Run this to deploy. Reads
              gcloud functions deploy listen_for_friend_requests \
            --runtime python38 \
            --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
            --trigger-resource "projects/findamare/databases/(default)/documents/friends/{user}/requests/{requester}"
              """

    #from database.user import db
    from database.notifications import PushNotifications

    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    person_requested = path_parts[1]
    requester = path_parts[3]

    #When a friend request is sent, we should tell the user via push notification
    PushNotifications.send_friend_request_to(person_requested, requester)

#TODO: add images (profile)
def listen_for_accepted_requests_OLD_DEPRECATED(data, context):
    """"
              # Run this to deploy. Reads
                  gcloud functions deploy listen_for_accepted_requests \
                --runtime python38 \
                --trigger-event "providers/cloud.firestore/eventTypes/document.update" \
                --trigger-resource "projects/findamare/databases/(default)/documents/friends/{user}/requests/{requester}"
                  """

    from database.notifications import PushNotifications
    from database.user import db
    from datetime import datetime
    from database.user import User

    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    person_requested = path_parts[1]
    requester = path_parts[3]

    dataHere = data["value"]['fields']
    didAccept = dataHere['accepted']['booleanValue']
    isNotable_requester = dataHere['isNotable']['booleanValue']
    requesters_name = dataHere['name']['stringValue']
    print(f"The data is is {dataHere} and did accept: {didAccept}")
    #
    requesters_profile_image_url = dataHere['profile_image_url']['stringValue']
    requested_person = User(id=person_requested)

    if didAccept:
        db.collection('friends').document(requester).collection('myFriends').document(person_requested).set({"friends_since": datetime.now(), "profile_image_url":requested_person.profile_image_url, "isNotable": requested_person.is_notable, "name": requested_person.name})
        db.collection('friends').document(person_requested).collection('myFriends').document(requester).set({"friends_since": datetime.now(), "profile_image_url": requesters_profile_image_url, "isNotable": isNotable_requester, "name": requesters_name})
        PushNotifications.acceptFriendRequestFrom(requester, person_requested)


#OLD friendship stricture, this might be deprecated or needs to be deleted.
def listen_for_added_friend_and_do_synastry(data, context):
    #Should add synastry chart to database when a new friend is added
    """"
          # Run this to deploy. Reads
              gcloud functions deploy listen_for_added_friend_and_do_synastry \
            --runtime python38 \
            --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
            --trigger-resource "projects/findamare/databases/(default)/documents/friends/{user1}/myFriends/{user2}"
              """

    from database.user import db
    from database.user import User
    path_parts = context.resource.split('/documents/')[1].split('/')
    user1 = path_parts[1]
    user2 = path_parts[3]

    user1 = User(id=user1)
    user2 = User(id=user2)

    #Compute synastry both ways (with user1 as the inner chart and with user1 as the outer chart)

    syn1 = user1.synastry(user2)
    syn2 = user2.synastry(user1)
    a1 = syn1.toArray() #aspects with user1 as the inner
    a2 = syn2.toArray() #aspects with user2 as the inner


    db.collection('synastry').document(user1.id).collection("outerChart").document(user2.id).set({'aspects': a1})
    db.collection('synastry').document(user2.id).collection("outerChart").document(user1.id).set({'aspects': a2})


    # TODO: Save all  synastry asepcts like you do placements
    #TODO: Add (placement only by sign attribute) for the 'NO ASPECTS' that still are aspect by sign

    # Saving all of their placements to my database . This is so that for example
    # User1 and User2 just became friends, User2 is a Scorpio Mars... User 1 needs to know he has a scorpio mars friend in database so
    # friends > user 1 > scorpio  > sun  (collection) > user2

    from astrology.NatalChart import planetToDict, aspectToDict

## adding user1's placements to user2's friends index
    for planet in user1.planets():
        planet_name = planet.id
        planet = planetToDict(planet)
        is_on_cusp = planet['is_on_cusp']
        angle = planet['angle']
        is_retrograde = planet['is_retrograde']
        sign = planet['sign']

        is_notable = user1.is_notable
        try:
            house = planet['house']
        except:
            house = None

        #Add placement to this friends database index
        db.collection(f'friends').document(f'{user2.id}').collection(f'{planet_name}').document('doc').collection(f'{sign}').document(user1.id).set({
            'is_on_cusp': is_on_cusp,
            'angle': angle,
            'is_retrograde': is_retrograde,
            'is_notable': is_notable,
            'house': house,
            'profile_image_url': user1.profile_image_url,
            'name': user1.name
        })

        #Now add house placements to friends database index
        if house is not None:
            db.collection(f'friends').document(f'{user2.id}').collection(f'{planet_name}').document('doc').collection(
                f'House{house}').document(user1.id).set({
                'is_on_cusp': is_on_cusp,
                'angle': angle,
                'is_retrograde': is_retrograde,
                'is_notable': is_notable,
                'house': house,
                'profile_image_url': user1.profile_image_url,
                'name': user1.name
            })



    ## doing the same now for user 2
    for planet in user2.planets():
        planet_name = planet.id
        planet = planetToDict(planet)
        is_on_cusp = planet['is_on_cusp']
        angle = planet['angle']
        is_retrograde = planet['is_retrograde']
        sign = planet['sign']

        is_notable = user1.is_notable

        try:
            house = planet['house']
        except:
            house = None

        # Add placement to this database index
        db.collection(f'friends').document(f'{user1.id}').collection(f'{planet_name}').document('doc').collection(f'{sign}').document(
            user2.id).set({
            'is_on_cusp': is_on_cusp,
            'angle': angle,
            'is_retrograde': is_retrograde,
            'is_notable': is_notable,
            'house': house,
            'profile_image_url': user2.profile_image_url,
            'name': user2.name
        })

        #Now add house placements to their friends index
        if house is not None:
            db.collection(f'friends').document(f'{user1.id}').collection(f'{planet_name}').document('doc').collection(
                f'House{house}').document(user2.id).set({
                'is_on_cusp': is_on_cusp,
                'angle': angle,
                'is_retrograde': is_retrograde,
                'is_notable': is_notable,
                'house': house,
                'profile_image_url': user2.profile_image_url,
                'name': user2.name
            })





    # Adding user 1's aspects to user 2's aspects index for their friends.
    #example: if user 1 has a Mars Conjunct Sun. User 2 needs to know he has a Mars Conjunct Sun friend so we add that index there
    #Basically user 2's friendlist is now sortable by aspect
    for aspect in user1.aspects():
        first_planet = aspect.first.id
        second_planet = aspect.second.id
        a = aspectToDict(aspect)
        a['profile_image_url'] =  user1.profile_image_url
        a['name'] = user1.name
        a['isReal'] = user1.isReal

        # Add placement to this database index
        db.collection(f'friends').document(f'{user2.id}').collection(f'{planet_name}').document('doc').collection(
            f'{second_planet}').document('doc').collection(f'{aspect.type}').document(user1.id).set(a)



    # Now doing the same for the other user

    for aspect in user2.aspects():
        first_planet = aspect.first.id
        second_planet = aspect.second.id
        a = aspectToDict(aspect)
        a['profile_image_url'] = user2.profile_image_url
        a['name'] = user2.name
        a['isReal'] = user2.isReal

        # Add placement to this database index
        db.collection(f'friends').document(f'{user1.id}').collection(f'{planet_name}').document('doc').collection(
            f'{second_planet}').document('doc').collection(f'{aspect.type}').document(user2.id).set(a)




# On user creation, create the myFriendCountShard to keep track of number of friends
def init_friend_counter(event, context):
    """
    Initialize a user's friend count shards when a new user is created.
    
    Deploy with:
    gcloud functions deploy init_friend_counter \
    --runtime python38 \
    --trigger-event providers/cloud.firestore/eventTypes/document.create \
    --trigger-resource "projects/findamare/databases/(default)/documents/users/{userID}"
    """
    
    user_id = context.resource.split('/documents/')[1].split('/')[1]
    doc_ref = db.collection('users').document(user_id)
    num_shards = 10
    col_ref = doc_ref.collection("myFriendsCountShards")

    for num in range(num_shards):
        col_ref.document(str(num)).set({"count": 0})
    
    doc_ref.update({"totalFriendCount": 0})


def update_friend_count(event, context):
    """
    Update the friend count shards when a new friend is added or removed.
    
    Deploy with:
    gcloud functions deploy update_friend_count \
    --runtime python38 \
    --trigger-event providers/cloud.firestore/eventTypes/document.write \
    --trigger-resource "projects/findamare/databases/(default)/documents/users/{userID}/myFriends/{friendID}"
    """
    
    import random 
    # Extracting the user_id from the document path
    resource_path = context.resource.split('/documents/')[1]
    path_parts = resource_path.split('/')
    user_id = path_parts[1]
    doc_ref = db.collection('users').document(user_id)
    num_shards = 10

    doc_id = random.randint(0, num_shards - 1)
    shard_ref = doc_ref.collection("myFriendsCountShards").document(str(doc_id))
    increment_value = 1 if event['value'] else -1
    shard_ref.update({"count": firestore.Increment(increment_value)})

    total = 0
    shards = doc_ref.collection("myFriendsCountShards").stream()
    for shard in shards:
        total += shard.to_dict().get("count", 0)

    doc_ref.update({"totalFriendCount": total})








def handle_failed_friend_request(data, context):
    """Triggered by the creation of a new document in the 'outgoingRequests' collection.
    
    gcloud functions deploy handle_failed_friend_request \
  --runtime python38 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}/outgoingRequests/{requestId}" \

    """

    from database.user import db
    import time
    from database.notifications import PushNotifications

    sender_id = context.resource.split('/')[6]
    receiver_id = context.resource.split('/')[8]

    # Reference to the incoming request
    incoming_request_ref = db.collection('users').document(receiver_id).collection('incomingRequests').document(sender_id)

    # Wait for 5 seconds before checking for the second write
    time.sleep(5)

    incoming_request = incoming_request_ref.get()
    if not incoming_request.exists:
        # If the incoming request doesn't exist after 5 seconds, delete the outgoing request
        outgoing_request_ref = db.collection('users').document(sender_id).collection('outgoingRequests').document(receiver_id)
        outgoing_request_ref.delete()
        return f"Deleted outgoing request from {sender_id} to {receiver_id} due to missing corresponding incoming request."
    else:
        #Notify user of a sent friend request
        PushNotifications.send_friend_request_to(receiver_id, sender_id)


    return f"Outgoing request from {sender_id} to {receiver_id} remains intact as the corresponding incoming request exists."






def handle_outgoing_request_deletion(data, context):
    """Triggered by the deletion of a document in the 'outgoingRequests' collection.
    
    
    gcloud functions deploy handle_outgoing_request_deletion \
  --runtime python38 \
  --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}/outgoingRequests/{requestId}" \
  --trigger-event "providers/cloud.firestore/eventTypes/document.delete"
"""
    from database.user import db
    sender_id = context.resource.split('/')[6]
    receiver_id = context.resource.split('/')[8]

    # Reference to the incoming request
    incoming_request_ref = db.collection('users').document(receiver_id).collection('incomingRequests').document(sender_id)

    # Delete the incoming request
    incoming_request_ref.delete()

    return f"Deleted incoming request from {receiver_id} due to deletion of outgoing request from {sender_id}."





def handle_incoming_request_deletion(data, context):
    """Triggered by the deletion of a document in the 'incomingRequests' collection.
    
    gcloud functions deploy handle_incoming_request_deletion \
  --runtime python38 \
  --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}/incomingRequests/{requestId}" \
  --trigger-event "providers/cloud.firestore/eventTypes/document.delete"
"""

    from database.user import db

    receiver_id = context.resource.split('/')[6]
    sender_id = context.resource.split('/')[8]

    # Reference to the outgoing request
    outgoing_request_ref = db.collection('users').document(sender_id).collection('outgoingRequests').document(receiver_id)

    # Delete the outgoing request
    outgoing_request_ref.delete()

    return f"Deleted outgoing request from {sender_id} due to deletion of incoming request from {receiver_id}."





def handle_incoming_request_acceptance(data, context):
    """Triggered by the update of a document in the 'incomingRequests' collection.
gcloud functions deploy handle_incoming_request_acceptance \
  --runtime python38 \
  --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}/incomingRequests/{requestId}" \
  --trigger-event "providers/cloud.firestore/eventTypes/document.update"
"""
    from database.user import db
    from datetime import datetime
    from database.user import User
    from database.notifications import PushNotifications

    
    receiver_id = context.resource.split('/')[6]
    sender_id = context.resource.split('/')[8]
    print(f"the data is ... {data['value']['fields']['status']['stringValue']}")

    
    # Check if the status has been updated to "accepted"
    if data['value']['fields']['status']['stringValue'] == 'friends':
        # Reference to the outgoing request
        outgoing_request_ref = db.collection('users').document(sender_id).collection('outgoingRequests').document(receiver_id)

        # Update the status of the outgoing request to "accepted"
        outgoing_request_ref.update({"status": "friends"})

        requested_person = User(id=receiver_id)
        #TODO -- Optimize this, because *no need* to create a User object to pull this data since technically we already read it when we listened on the branch. see the old friendship lisenter above to understand
        sender_user = User(id=sender_id)


        # Add the official friendship to both users' records (if needed)
        # ...
        db.collection('users').document(sender_id).collection('myFriends').document(receiver_id).set({"friends_since": datetime.now(), "profile_image_url":requested_person.profile_image_url, "isNotable": requested_person.is_notable, "name": requested_person.name})
        db.collection('users').document(receiver_id).collection('myFriends').document(sender_id).set({"friends_since": datetime.now(), "profile_image_url": sender_user.profile_image_url, "isNotable": sender_user.is_notable, "name": sender_user.name})
        # Give them both  stars 
        db.collection('users').document(sender_id).update({'stars': firestore.Increment(9)})
        db.collection('users').document(receiver_id).update({'stars': firestore.Increment(9)})
        PushNotifications.acceptFriendRequestFrom(sender_id,receiver_id)

    return f"Updated outgoing request status for {sender_id} due to acceptance of incoming request by {receiver_id}."

#TODO: delete synastries too
def listen_for_removed_friend(data, context):
    """"
      # Run this to deploy. Reads
          gcloud functions deploy listen_for_removed_friend \
        --runtime python37 \
        --trigger-event "providers/cloud.firestore/eventTypes/document.delete" \
        --trigger-resource "projects/findamare/databases/(default)/documents/friends/{A}/myFriends/{B}"
          """

    # Let user 'A' remove user 'B' as a friend using mobile app.
    # If 'A' removes 'B' as a friend. (Trigger) /friends/A/myFriends/B (detect a deletion)
        # WE should 1. remove 'A' from 'B' and 2. remove friend requests from both (in case they exist)

    from database.user import db
    path_parts = context.resource.split('/documents/')[1].split('/')
    user_A = path_parts[1]
    user_B = path_parts[3]

    print(f"Should be deleting {user_A} from {user_B} friend list and 2-way friend request")
    db.collection("friends").document(user_B).collection("myFriends").document(user_A).delete()
    db.collection("friends").document(user_A).collection("requests").document(user_B).delete()
    db.collection("friends").document(user_B).collection("requests").document(user_A).delete()




def listen_for_deleted_user(data, context):
    """"
  # Run this to deploy. Reads
      gcloud functions deploy listen_for_deleted_user \
    --runtime python37 \
    --trigger-event "providers/cloud.firestore/eventTypes/document.delete" \
    --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}"
      """

    import analytics.app_data as analytics
    from analytics.app_data import less_user

    less_user()

    try:
        old_user_data = data['oldValue']
        old_sex = old_user_data['fields']['sex']['stringValue']

        if old_sex == "male":
            analytics.less_male()
        elif old_sex == 'female':
            analytics.less_female()
        elif old_sex == 'transfemale':
            analytics.less_trans_female()
        elif old_sex == 'transmale':
            analytics.less_trans_male()
        elif old_sex == 'non-binary':
            analytics.less_non_binary()
        else:
            pass

    except Exception as e:
        print(f"Could not delete gender count from database with error {e}")


def handle_failed_wink(data, context):
    """Triggered by the creation of a new document in the 'outgoingWinks' collection. (When a user winks at another)
    
    gcloud functions deploy handle_failed_wink \
  --runtime python38 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
  --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}/outgoingWinks/{receiverID}" \

    """

    from database.user import db
    import time
    from database.notifications import PushNotifications

    sender_id = context.resource.split('/')[6]
    receiver_id = context.resource.split('/')[8]

    # Reference to the incoming wink
    incoming_request_ref = db.collection('users').document(receiver_id).collection('incomingWinks').document(sender_id)

    # Send notification to reciever 
    PushNotifications.winked_at(receiver_id, sender_id)

    # Wait for 5 seconds before checking for the second write
    time.sleep(5)

    incoming_request = incoming_request_ref.get()
    if not incoming_request.exists:
        # If the incoming request doesn't exist after 5 seconds, delete the outgoing request
        outgoing_request_ref = db.collection('users').document(sender_id).collection('outgoingWinks').document(receiver_id)
        outgoing_request_ref.delete()
        return f"Deleted outgoing wink from {sender_id} to {receiver_id} due to missing corresponding incoming wink."

    return f"Outgoing wink from {sender_id} to {receiver_id} remains intact as the corresponding incoming wink exists."



def messaging_token(request):
    
    """

This returns a token that the frontend can use to authenticate with the backend to send messages. 
    This token is generated from the user_id and has no expiration date.

- Request Parameters: 
     - userId : The id of the user who is sending the message.


 Deployment:
     gcloud functions deploy messaging_token \
--runtime python37 --trigger-http  --security-level=secure-always --allow-unauthenticated

Get Url to endpoing: 
gcloud functions describe messaging_token 


    """

    from Messaging.streamBackend import get_token_from_user_id

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'userId' in request_json:
            userId = request_json['userId']
            response = {"success": True, "data": {"token": get_token_from_user_id(userId)}}
            resp = jsonify(status=200, **response)
            resp.headers.set('Access-Control-Allow-Origin','*')
            resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
            return resp
    else: 
        resp = {"success": False, "error": {"code": 401, "description": "Please provide a user id in the request body."}}
        resp = jsonify(status=401, **resp)
        resp.headers.set('Access-Control-Allow-Origin','*')
        resp.headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        resp.headers.set("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        return resp

    
"""Returns the Astrological Profile of the user based on input data.

- Request Parameters:
     - name (String) : The name of the user 
     - gender (String) : male, female, or other 
     - latitude (Double) : Latitude of birth location
     - longitude (Double) : Longitude of birth location 
     - birthdayInSecondsSince1970 (Double) : Birthday of the user in UTC. This should be the timestamp: seconds since 1970
     - knowsBirthtime (Bool): Whether the user knows his/her birthtime

 Deployment:
     gcloud functions deploy predict_traits \
--runtime python38 --trigger-http --security-level=secure-always --allow-unauthenticated

Get Url to endpoint: 
gcloud functions describe predict_traits
"""
def predict_traits(request): 
    """ gcloud functions deploy predict_traits \
    --runtime python38 \
    --trigger-http \
    --allow-unauthenticated
    --timeout=540s"""
    from database.Location import Location
    from datetime import datetime 
    from prompts.astrology_traits_generator import AstrologyTraitsGenerator
    


    if request.method != 'POST': 
         return jsonify(success=False,
                           error={
                               'code': 405,
                               'description': "Only POST request allowed here.",
                               'why': 'I just decided this.',
                               'trace': traceback.format_exc()}
                           )

    req_data = request.get_json()

    # Extract the variables from the parsed JSON data
    # Assuming all the fields are mandatory, make sure to add error handling for missing fields.
    try:
        name = req_data["name"]
        gender = req_data["gender"]
        latitude = float(req_data["latitude"])  # Convert string to float
        longitude = float(req_data["longitude"])  # Convert string to float
        knowsBTime = req_data["knowsBirthtime"]
        birthday_in_seconds_since_1970 = float(req_data["birthdayInSecondsSince1970"])  # Convert string to float
    except KeyError as e:

        return jsonify(success=False,
                           error={
                               'code': 400,
                               'description': f"Missing required parameter: {e.args[0]}",
                               'why': 'I just decided this.',
                               'trace': traceback.format_exc()}
                           )
        
    
    except ValueError as e:
        

        return jsonify(success=False,
                           error={
                               'code': 400,
                               'description': f"Invalid data format for one of the parameters. Error: {str(e)}",
                               'why': 'I just decided this.',
                               'trace': traceback.format_exc()}
                           )


    loc=Location(latitude=float(latitude), longitude=float(longitude))

    user = User(do_not_fetch=True,  birthday = datetime.utcfromtimestamp(birthday_in_seconds_since_1970), name=name, known_time=knowsBTime, hometown=loc)
    n = user.natal() # Generates the natal chart 
    user.name = name
    user.sex = gender 
    astroData = user.astroDataForAPI()


    # Now send the prompt to LLM 
    
    trait_generator = AstrologyTraitsGenerator()
    traits = trait_generator.predict_traits(name=user.name, gender=user.sex, astro_data=astroData)
   

    # For now, echo the same data as response to confirm parsing was successful
    response_data = {
      "traits": traits, 
        "name": name,
        "gender": gender,
       "latitude": latitude,
        "longitude": longitude,
        "birthdayInSecondsSince1970": birthday_in_seconds_since_1970, 
        "knowsBirthTime": knowsBTime, 
    
       # "natal": n
    }
    return jsonify(status=200, **response_data)


"""Returns behavioral statements based on the Astrological Profile of the user based on input data.

- Request Parameters:
     - name (String) : The name of the user 
     - gender (String) : male, female, or other 
     - latitude (Double) : Latitude of birth location
     - longitude (Double) : Longitude of birth location 
     - birthdayInSecondsSince1970 (Double) : Birthday of the user in UTC. This should be the timestamp: seconds since 1970
     - knowsBirthtime (Bool): Whether the user knows his/her birthtime

 Deployment:
     gcloud functions deploy predict_traits \
--runtime python38 --trigger-http --security-level=secure-always --allow-unauthenticated

Get Url to endpoint: 
gcloud functions describe predict_traits
"""
def predict_statements(request): 
    """ gcloud functions deploy predict_statements \
    --runtime python38 \
    --trigger-http \
    --allow-unauthenticated \
    --timeout=540s"""
    from database.Location import Location
    from datetime import datetime 
    from prompts.astrology_traits_generator import AstrologyTraitsGenerator
    


    if request.method != 'POST': 
         return jsonify(success=False,
                           error={
                               'code': 405,
                               'description': "Only POST request allowed here.",
                               'why': 'I just decided this.',
                               'trace': traceback.format_exc()}
                           )

    req_data = request.get_json()

    # Extract the variables from the parsed JSON data
    # Assuming all the fields are mandatory, make sure to add error handling for missing fields.
    try:
        name = req_data["name"]
        gender = req_data["gender"]
        latitude = float(req_data["latitude"])  # Convert string to float
        longitude = float(req_data["longitude"])  # Convert string to float
        knowsBTime = req_data["knowsBirthtime"]
        birthday_in_seconds_since_1970 = float(req_data["birthdayInSecondsSince1970"])  # Convert string to float
    except KeyError as e:

        return jsonify(success=False,
                           error={
                               'code': 400,
                               'description': f"Missing required parameter: {e.args[0]}",
                               'why': 'I just decided this.',
                               'trace': traceback.format_exc()}
                           )
        
    
    except ValueError as e:
        

        return jsonify(success=False,
                           error={
                               'code': 400,
                               'description': f"Invalid data format for one of the parameters. Error: {str(e)}",
                               'why': 'I just decided this.',
                               'trace': traceback.format_exc()}
                           )


    loc=Location(latitude=float(latitude), longitude=float(longitude))

    try:
        user = User(do_not_fetch=True, birthday=datetime.utcfromtimestamp(birthday_in_seconds_since_1970), name=name, known_time=knowsBTime, hometown=loc)
        statements = user.personality_statements()

    # For now, echo the same data as response to confirm parsing was successful
        response_data = {
        "statements": statements,
        "name": name,
        "gender": gender,
        "latitude": latitude,
        "longitude": longitude,
        "birthdayInSecondsSince1970": birthday_in_seconds_since_1970,
        "knowsBirthTime": knowsBTime
    }
        return jsonify(status=200, **response_data)

    except Exception as e:
        return jsonify(success=False,
                   error={
                       'code': 400,
                       'description': f"{str(e)}",
                       'why': 'An error occurred while processing the request.',
                       'trace': traceback.format_exc()
                   })

    


""" Helper function for placement read to update interpretation """


def update_interpretation(user_id, planet, interpretation):
    from database.user import db 
    user_ref = db.collection('users').document(user_id)
    natal_chart_ref = user_ref.collection('public').document('natal_chart')

    update_data = {
        f'interpretations.{planet}': interpretation
    }

    natal_chart_ref.update(update_data)

def update_aspect_interpretation(user_id, name, interpretation, requester_id=None):
    from database.user import db 
    
    requester_user_ref = db.collection('users').document(requester_id)
    user_ref = db.collection('users').document(user_id)

    # update 
    natal_chart_ref = user_ref.collection('public').document('natal_chart')
    update_data = {
           f'aspects_interpretations.{name}': interpretation
       }
    natal_chart_ref.update(update_data)
    
    
    #decrement 
    requester_user_ref.update({'stars': firestore.Increment(-1)})


    # fix this: update_aspect_interpretation_and_deduct_stars(db.transaction(), user_id, name, interpretation, requester_id)



""""
@firestore.transactional
def update_aspect_interpretation_and_deduct_stars(transaction: Transaction, user_id: str, name: str, interpretation: str, requester_id: str):
   user_ref = db.collection('users').document(requester_id)
   user_ref_for_reading = db.collection('users').document(user_id)
   natal_chart_ref = user_ref_for_reading.collection('public').document('natal_chart')

   user_snapshot = user_ref.get(transaction=transaction)
   natal_chart_snapshot = natal_chart_ref.get(transaction=transaction)
   print(f"user_snapshot data: {user_snapshot.to_dict()}")
   print(f"natal_chart_snapshot data: {natal_chart_snapshot.to_dict()}")


   if user_snapshot.exists and natal_chart_snapshot.exists:
       update_data = {
           f'aspects_interpretations.{name}': interpretation
       }
       stars = user_snapshot.get('stars')
       if stars is not None and stars >= 1:
           print(f"Stars before deduction: {stars}")
           update_data['stars'] = stars - 1
           print(f"Stars after deduction: {update_data['stars']}")
           transaction.update(natal_chart_ref, update_data)
       else:
           # If stars are not sufficient, raise an exception to abort the transaction
           raise ValueError("Not enough stars")
   else:
       # If either user or natal chart does not exist, raise an exception to abort the transaction
       raise ValueError("User or natal chart not found")
"""






""" Interprets a particular placement (sign, planet, house)"""
#TODO: make option for genderless in the prompt, we use 'person' for now thus far but we need to see how the synastry changes when we do this
def placement_read(request):
    """
    POST: Retrieves astrology interpretation for a specific placement based on input parameters.
    url: https://us-central1-findamare.cloudfunctions.net/placement_read
    Parameters in REST API Call:
    - gender: (optional) 'male' or 'female'. If missing, defaults to 'person'.
    - planet: (required) Name of the planet or celestial body (e.g., 'North Node').
    - sign: (required) Astrological sign (e.g., 'Leo').
    - house: (optional) Astrological house as an ordinal number (e.g., '1st', '2').
    - user_id: (optional) User identifier.

    JSON Response:
    {
        "success": HTTP status code,
        "interpretation": String interpretation,
        "error": Error message if applicable
    }
    
    Example: curl -X POST https://us-central1-findamare.cloudfunctions.net/placement_read -H "Content-Type: application/json" -d '{"gender": "male", "planet": "Sun", "sign": "Cancer/Leo Cusp", "house": "7"}'
    Deploy using the following command:
    gcloud functions deploy placement_read \
    --runtime python38 \
    --trigger-http \
    --allow-unauthenticated

    
     curl -X POST localhost:8080/placement_read -H "Content-Type: application/json" -d '{"gender": "male", "planet": "Sun", "sign": "Cancer/Leo Cusp", "house": "7"}'



    For testing: 
    /Library/Frameworks/Python.framework/Versions/3.7/bin/functions-framework --target=placement_read --signature-type=http

    """
    if request.method != 'POST': 
         return jsonify(success=False,
                           error={
                               'code': 405,
                               'description': "Only POST request allowed here.",
                               'why': 'I just decided this.',
                               'trace': traceback.format_exc()}
                           )
    
    

    req_data = request.get_json()
    gender = req_data.get('gender', 'person').lower()
    planet = req_data.get('planet')
    sign = req_data.get('sign')
    house_num = req_data.get('house', "")
    user_id = req_data.get('user_id', None)

    
    # Convert house number to ordinal string (e.g., '1' -> '1st')
    if house_num.isdigit():
        house_num = "{}{}".format(house_num, 'th' if 4 <= int(house_num) % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(int(house_num) % 10, 'th'))

    try:
        
        from prompts.astrology_traits_generator import PlacementInterpretationsGenerator
        reader = PlacementInterpretationsGenerator()
        interpretation = reader.interpret_placement(gender, planet, sign, house_num)

        # Optional: Write to Firestore if user_id is provided
        if user_id:
            update_interpretation(user_id, planet, interpretation)

        
            
        return jsonify(success=True,
                       interpretation=interpretation,
                       prompt=reader.prompt
                        
                           )
        


    except Exception as e:
        return jsonify(success=False, error=str(e))



def aspect_read(request):
    """
    POST: Retrieves astrology interpretation for a specific placement based on input parameters.
    url: https://us-central1-findamare.cloudfunctions.net/aspect_read
    Parameters in REST API Call:
    - gender: (optional) 'male' or 'female'. If missing, defaults to 'person'.
    - planet1: (required) Name of the planet or celestial body (e.g., 'North Node').
    - type: (required) Astrological aspect type  (e.g., 'Square').
    - planet2: (required) Name of the planet or celestial body (e.g., 'North Node').
    - name: (required) Name of the aspect (e.g., 'Sun Moon')
    - orb: (required) Int
    - user_id: user_id for the user so that we can write this description to them 
    - requesting_user_id: the user that is requesting this information 

    JSON Response:
    {
        "success": HTTP status code,
        "interpretation": String interpretation,
        "error": Error message if applicable
    }
    
    Example: curl -X POST https://us-central1-findamare.cloudfunctions.net/aspect_read -H "Content-Type: application/json" -d '{"gender": "male", "planet1": "Sun", "type": "Square", "planet2": "Moon", orb: 4}'
    Deploy using the following command:
    gcloud functions deploy aspect_read \
    --runtime python38 \
    --trigger-http \
    --allow-unauthenticated \
    --timeout=540s

    curl -X POST https://us-central1-findamare.cloudfunctions.net/aspect_read -H "Content-Type: application/json" -d '{"gender": "male", "planet1": "Sun", "type": "Square", "planet2": "Moon", orb: 4, name: "Mars Jupiter", "user_id": "ei8U2avSdYZCijlCmfMbsvLjUwD2"}'

    
     curl -X POST localhost:8080/aspect_read -H "Content-Type: application/json" -d '{"gender": "male", "planet1": "Sun", "type": "Square", "planet2": "Moon", orb: 4}'

    curl -X POST https://us-central1-findamare.cloudfunctions.net/aspect_read -H "Content-Type: application/json" -d '{"gender": "male", "planet1": "Mars", "planet2": "Jupiter", "type": "Square", "user_id": "ei8U2avSdYZCijlCmfMbsvLjUwD2", "orb": 4}'

    For testing: 
    /Library/Frameworks/Python.framework/Versions/3.7/bin/functions-framework --target=aspect_read --signature-type=http

    """
    if request.method != 'POST': 
         return jsonify(success=False,
                           error={
                               'code': 405,
                               'description': "Only POST request allowed here.",
                               'why': 'I just decided this.',
                               'trace': traceback.format_exc()}
                           )
    
    

    req_data = request.get_json()
    gender = req_data.get('gender', 'person').lower()
    planet1 = req_data.get('planet1')
    planet2 = req_data.get('planet2')
    aspectType = req_data.get('type')
    name = req_data.get('name')
    orb = req_data.get('orb')
    user_id = req_data.get('user_id', None)
    requesting_user_id = req_data.get('requesting_user_id', user_id)

    if not check_stars(requesting_user_id):
        print("Not enough stars")
        return jsonify(success=False, error="You don't have enough stars!")

    

    
    try:
        
        from prompts.astrology_traits_generator import PlacementInterpretationsGenerator
        reader = PlacementInterpretationsGenerator()
        print(f"{requesting_user_id} is requesting {user_id}")
        interpretation = reader.interpret_aspect(gender, planet1, aspectType, planet2, orb)

        # Optional: Write to Firestore if user_id is provided
        if user_id:
            update_aspect_interpretation(user_id, name, interpretation, requester_id=requesting_user_id)

        
            
        return jsonify(success=True,
                       interpretation=interpretation,
                       prompt=reader.prompt
                        
                           )
        


    except Exception as e:
        return jsonify(success=False, error=str(e))


def check_stars(user_id, amount=1):
    """ Checks if the user has enough stars to do this """
    user_ref = db.collection('users').document(user_id)

    # Get the document snapshot
    user_doc = user_ref.get()

    # Check if the document exists
    if user_doc.exists:
        # Get the 'stars' property
        try: 
            stars = user_doc.get('stars')
        except: 
            return False

        # Check if 'stars' is at least 1
        if stars is not None and stars >= amount:
            return True
    return False

def message_dasha(request):
    """
    POST: Sends a message using DashaChatBot.

    URL: https://us-central1-findamare.cloudfunctions.net/message_dasha

    Parameters in JSON payload:
    - userID: User identifier.
    - message: Message to be sent.

    JSON Response:
    {
        "success": true or false,
        "message": "Message sent successfully" or error message
    }

    Example:
    curl -X POST https://us-central1-findamare.cloudfunctions.net/message_dasha \
        -H "Content-Type: application/json" \
        -d '{"userID": "ZH17wkDgkIVFqQ2F9wtwcRPi5oo1", "message": "Hello, Dasha!"}'

    Deploy using the following command:
    gcloud functions deploy message_dasha \
        --runtime python38 \
        --trigger-http \
        --allow-unauthenticated  \
        --timeout=540s
        
    """
    from prompts.astrology_traits_generator import DashaChatBot

    
    try:
        request_json = request.get_json(silent=True)

        # Extracting parameters from the JSON payload
        user_id = request_json.get('userID')
        message = request_json.get('message')

        print(f"The user id {user_id} and message: {message}")

        # Check if they have enough stars
        
        if not check_stars(user_id):
            print("Not enough stars")
            send_message_to_user(user_id, "You don't have enough ⭐️'s to message me. 😭 😭 😭. You can get more stars by adding friends or engaging with the app! If I see you tomorrow, you might get some for free. 😏😏😏")
            return jsonify(success=False, error="You don't have enough stars!")
        
        print("sending messsage to dasha")

        # Call the sendMessageFrom method
        DashaChatBot.sendMessageFrom(user_id, message)

        # Increment Sent Dasha Message
        db.collection('users').document(user_id).update({'sentDashaMessages': firestore.Increment(1)}) 

        # Decrement Stars
        db.collection('users').document(user_id).update({'stars': firestore.Increment(-1)})

        # Return a success response
        return jsonify(success=True )
        
        

    except Exception as e:
        # Handle errors
        return jsonify(success=False,
                           error={
                               'code': 400,
                               'description': str(e)}
                           ) 


def message_dasha_about_another(request):
    """
    POST: Sends a message using DashaChatBot.

    URL: https://us-central1-findamare.cloudfunctions.net/message_dasha_about_another

    Parameters in JSON payload:
    - requestingUserID: User identifier of the user who is requesting the synastry
    - targetUserID: The user whose information will be read. e.g. Micheal is chating about Grace with Dasha
    

    JSON Response:
    {
        "success": true or false,
        "message": "Message sent successfully" or error message
    }

    Example:
    curl -X POST https://us-central1-findamare.cloudfunctions.net/message_dasha \
        -H "Content-Type: application/json" \
        -d '{"userID": "ZH17wkDgkIVFqQ2F9wtwcRPi5oo1", "message": "Hello, Dasha!"}'

    Deploy using the following command:
    gcloud functions deploy message_dasha \
        --runtime python38 \
        --trigger-http \
        --allow-unauthenticated  \
        --timeout=540s
        
    """
    from prompts.astrology_traits_generator import DashaChatBot

    
    try:
        request_json = request.get_json(silent=True)

        # Extracting parameters from the JSON payload
        requestingUserID = request_json.get('requestingUserID')
        targetUserID = request_json.get('targetUserID')

        firstUser = User(id=requestingUserID)
        secondUser = User(id=targetUserID)

        # Check if they have enough stars
        
        
        # message should contain info about the other person 
        print("sending messsage to dasha")

        # Call the sendMessageFrom method
        DashaChatBot.sendMessageFrom(user_id, message)

        # Increment Sent Dasha Message
        db.collection('users').document(user_id).update({'sentDashaMessages': firestore.Increment(1)}) 

        # Decrement Stars
        db.collection('users').document(user_id).update({'stars': firestore.Increment(-1)})

        # Return a success response
        return jsonify(success=True )
        
        

    except Exception as e:
        # Handle errors
        return jsonify(success=False,
                           error={
                               'code': 400,
                               'description': str(e)}
                           ) 
