from flask import jsonify
from database.user import User
import traceback
"""
PATH_TO_FIR_CREDENTIALS = 'amare-firebase.json'
cred = credentials.Certificate(PATH_TO_FIR_CREDENTIALS)
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
"""

##Hide this, do not expose this
SECRET = "O6012599956O6012598567K4048252227M9176990590"



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
     gcloud functions deploy hello \
--runtime python39 --trigger-http --allow-unauthenticated

Delete:
gcloud functions delete hello

Get url to end point
gcloud functions describe hello


Returns the user data  

- Request Parameters: 
     - SECRET (String) : secret id used to authenticate for the admin api 
     - id:   (String)   user id of user requesting 
     
- Returns 
     - success (Bool) : true or false of whether the response was successful. This will be in any request 
     - error: (JSON) 
                - code (INT)                :       Error code , (400 Bad request)
                - description (String)      :       Description of the error 

'''


def go(request):


    try:
        data = request.get_json(force=True)
        try:

            secret = data["secret"]

            if not (secret == SECRET):
                return jsonify(success=False,
                           error=jsonify(
                                    code=401,
                                     description="UNAUTHORIZED. Failed to authenticate, invalid secret key.")
                           )

            try:
                id = data["id"]

                try:
                    user = User(id=id)

                    #User Information
                    name = user.name
                    return jsonify(
                        success=True,
                        name=name
                    )

                except:
                    return jsonify(success=False,
                                   error=jsonify(
                                       code=404,
                                       description="USER NOT FOUND. The user does not exist.")
                                   )



            except:  # nn auth data providied
                return jsonify(success=False,
                               error=jsonify(
                                   code=400,
                                   description="BAD REQUEST. Missing user id.")
                               )

        except:  #nn auth data providied
            return jsonify(success=False,
                           error=jsonify(
                                    code=400,
                                     description="BAD REQUEST. Failed to authenticate, missing the secret key.")
                           )

    except:
        return jsonify(success=False,
                       error=jsonify(
                           code=400,
                           description="BAD REQUEST. Could not understand request.")
                       )


def user(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
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

    if secret == SECRET:

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

            return jsonify(success=True,
                           user={
                               'name': user.name
                           })

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









