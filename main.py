from flask import jsonify
from database.user import User
import traceback
from secret import api_keys



from json import dumps
from flask import make_response

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





# Converts strings added to /messages/{pushId}/original to uppercase
#- Creates a natal chart for the user and adds it to the database when they sign up
#- Checks user gender and +1 for gender ( to keep statistics on amount of women/men on platform)
def monitor_user_data(data, context):
    """"

# Run this to deploy. Reads
    gcloud functions deploy monitor_user_data \
  --runtime python38 \
  --trigger-event "providers/cloud.firestore/eventTypes/document.update" \
  --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}"

    """
    from database.user import db
    from database.Location import Location
    import iso8601
    import analytics.app_data as analytics

    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])

    affected_doc = db.collection(collection_path).document(document_path)
    id = document_path


    trigger_resource = context.resource
    print('***Function triggered by change to: %s and id %s: ' % (trigger_resource, id))

    updated_attributes =  data["updateMask"]["fieldPaths"] #returns list of attributes updated on commit in firebase  ex: ['hometown']
    user_data = data["value"]
    old_user_data = data['oldValue']

    print("The updated attributes are: ")
    print(updated_attributes)


    #chart should update if 'hometown' , 'birthday', 'known_time', are modified.
    # and if both hometown and birthday exist in the database, if known_time isn't assume false.

    if 'sex' in updated_attributes:
        new_sex = user_data['fields']['sex']['stringValue']
        try:
            old_sex = old_user_data['fields']['sex']['stringValue']

            if old_sex != new_sex:    #the sex changed so we should decrment the old one and increment new one

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

                if new_sex == "male":
                    analytics.new_male()
                elif new_sex == 'female':
                    analytics.new_female()
                elif new_sex == 'transfemale':
                    analytics.new_trans_female()
                elif new_sex == 'transmale':
                    analytics.new_trans_male()
                elif new_sex == 'non-binary':
                    analytics.new_non_binary()
                else:
                    pass

        except:
            # No old value found for sex so it's probably newly created
            if new_sex == "male":
                analytics.new_male()
            elif new_sex == 'female':
                analytics.new_female()
            elif new_sex == 'transfemale':
                analytics.new_trans_female()
            elif new_sex == 'transmale':
                analytics.new_trans_male()
            elif new_sex == 'non-binary':
                analytics.new_non_binary()
            else:
                pass




    if 'hometown' in updated_attributes or 'birthday' in updated_attributes or 'known_time' in updated_attributes:

        try:
            print(f"the FULL user data is {user_data}")
            lat = user_data['fields']['hometown']['mapValue']['fields']['latitude']['doubleValue']
            lon = user_data['fields']['hometown']['mapValue']['fields']['longitude']['doubleValue']
            location = Location(latitude=lat, longitude=lon)


            bday = user_data['fields']['birthday']['mapValue']['fields']['timestamp']['timestampValue']
            date = iso8601.parse_date(bday) #converts the timestamp String into a datetime object
            try:
                known_time = user_data['fields']['known_time']['booleanValue']
            except:
                known_time = False

            user = User(id=id,
                        do_not_fetch=True,
                        hometown=location,
                        birthday=date,
                        known_time=known_time
                        )
            # Set it in database now
            user.set_natal_chart()
        except Exception as error:
            print(f"This data does not exist in the database yet or some error:  {error}")



def listen_for_new_user(data, context):
    """"
  # Run this to deploy. Reads
      gcloud functions deploy listen_for_new_user \
    --runtime python38 \
    --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
    --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}"
      """

    from analytics.app_data import new_user
    from database.user import db
    from database.Location import Location
    import iso8601
    from icecream import ic



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
            try:
                known_time = dataHere['known_time']['booleanValue']
            except:
                known_time = False

            user = User(id=id,
                        do_not_fetch=True,
                        hometown=location,
                        birthday=date,
                        known_time=known_time
                        )
            # Set it in database now
            user.set_natal_chart()
            new_user()
        except Exception as error:
            print(f"This data does not exist in the database yet or some error:  {error}")

    if 'sex' in dataHere:

        try:

           old_sex = dataHere

            if True:    #the sex changed so we should decrment the old one and increment new one

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

                if new_sex == "male":
                    analytics.new_male()
                elif new_sex == 'female':
                    analytics.new_female()
                elif new_sex == 'transfemale':
                    analytics.new_trans_female()
                elif new_sex == 'transmale':
                    analytics.new_trans_male()
                elif new_sex == 'non-binary':
                    analytics.new_non_binary()
                else:
                    pass

        except:
            # No old value found for sex so it's probably newly created
            if new_sex == "male":
                analytics.new_male()
            elif new_sex == 'female':
                analytics.new_female()
            elif new_sex == 'transfemale':
                analytics.new_trans_female()
            elif new_sex == 'transmale':
                analytics.new_trans_male()
            elif new_sex == 'non-binary':
                analytics.new_non_binary()
            else:
                pass

    else:  #Update analytics because this is probably a new user
        pass

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


def listen_for_new_natal_chart(data, context):
    # Triggered when a new natal chart has been added to the database
    # Should add the user to the indexes of each aspect ; e.g -- if they're a sun in scorpio, add them to it, etc
    # Should add them to the aspect type too

    from database.user import db
    from database.user import User

    """"
     # Run this to deploy. Reads
         gcloud functions deploy listen_for_new_natal_chart \
       --runtime python38 \
       --trigger-event "providers/cloud.firestore/eventTypes/document.create" \
       --trigger-resource "projects/findamare/databases/(default)/documents/users/{userId}/public/natal_chart"
         """



    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    document_path = '/'.join(path_parts[1:])
    id = path_parts[1] #ID of the user the natal chart belongs too

    natal_chart_doc = db.collection(collection_path).document(document_path).get()#Document reference object
    natal_dict = natal_chart_doc.to_dict()

    print(f"The natal chart doc is : {natal_chart_doc} and dictionary is {natal_dict}")

    #Going through the planets and adding each placmenet to the index; e.g. if Sun in Cancer
    # -- add user to Sun / Cancer aspect
    # data structure: 
    #       /placements (collection)
    #           / <planet> (collection)
    #               / <cancer> (collection)
    #                   / <user ID> (document)
    #                       /


    user = User(id=id)

    #TODO: Add house number to planet placement
    planets = natal_dict['planets']
    for planet in planets:
        is_on_cusp = planet['is_on_cusp']
        angle = planet['angle']
        is_retrograde = planet['is_retrograde']
        sign = planet['sign']
        planet_name = planet['name']
        is_notable = user.is_notable

        #Add placement to this database index
        db.collection(f'placements').document(f'{planet_name}').collection(f'{sign}').document(id).set({
            'is_on_cusp': is_on_cusp,
            'angle': angle,
            'is_retrograde': is_retrograde,
            'is_notable': is_notable
        })






#Winked vs Winker in database --> winks / {winked} / peopleWhoWinked / {winker}
def listen_for_winks(data, context):
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






def listen_for_accepted_requests(data, context):
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

    path_parts = context.resource.split('/documents/')[1].split('/')
    collection_path = path_parts[0]
    person_requested = path_parts[1]
    requester = path_parts[3]

    dataHere = data["value"]['fields']
    didAccept = dataHere['accepted']['booleanValue']
    print(f"The data is is {dataHere} and did accept: {didAccept}")

    if didAccept:
        db.collection('friends').document(requester).collection('myFriends').document(person_requested).set({"friends_since": datetime.now()})
        db.collection('friends').document(person_requested).collection('myFriends').document(requester).set({"friends_since": datetime.now()})
        PushNotifications.acceptFriendRequestFrom(requester, person_requested)


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
















