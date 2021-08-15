from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from flask import jsonify
from user import User
"""
PATH_TO_FIR_CREDENTIALS = 'amare-firebase.json'
cred = credentials.Certificate(PATH_TO_FIR_CREDENTIALS)
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
"""

from flask import escape
##Hide this, do not expose this
SECRET = "O6012599956O6012598567K4048252227M9176990590"

def hello(request):
    #data = request.get_json(force=True)
    """HTTP Cloud Function.
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


    """

    name = ""
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        name = request.data
    elif content_type == 'text/plain':
        name = request.data
    elif content_type == 'application/x-www-form-urlencoded':
        name = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    return 'Hello {}!'.format(escape(name))
""""
    try:

        sample1 = data['sample1']
        sample2 = data['sample2']
        sample3 = data['sample3']
    except:
        sample1 = ""
        sample2 = ""
        sample3 = ""

    sample1String = 'The sample data posted  is: {}'.format(sample1)
    sample2String = 'The sample data posted  is: {}'.format(sample2)
    sample3String = 'The sample data posted  is: {}'.format(sample3)
    return 'Welcome to the Amāre API.\n\n (c) 2021 Amāre Corporation\n' +  sample2String + '\n' + sample3String
"""

## Admin Functions ...

# Get's the natal chart of a user by user id.
'''  
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


def get(request):


    try:
        data = request.get_json(force=True)
        try:

            secret = request.args.get("secret", "") #data["SECRET"]

            if not (secret == SECRET):
                return jsonify(success=False,
                           error=jsonify(
                                    code=401,
                                     description="UNAUTHORIZED. Failed to authenticate, invalid secret key.")
                           )

            try:
                id = request.args.get("id", "") #data["id"]

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










"""
# Converts strings added to /messages/{pushId}/original to uppercase
def new_user(data, context):
    #path_parts = context.resource.split('/documents/')[1].split('/')
    #collection_path = path_parts[0]
    #document_path = '/'.join(path_parts[1:])

    affected_doc = db.collection(collection_path).document(document_path)

    cur_value = data["value"]["fields"]["original"]["stringValue"]
    new_value = cur_value.upper()

    if cur_value != new_value:
        print(f'Replacing value: {cur_value} --> {new_value}')
        affected_doc.set({
            u'original': new_value
        })
    else:
        # Value is already upper-case
        # Don't perform a second write (which can trigger an infinite loop)
        print('Value is already upper-case.')

"""




def hello_method(request):
    """ Responds to a GET request with "Hello world!". Forbids a PUT request.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    from flask import abort

    if request.method == 'GET':
        return 'Hello World!'
    elif request.method == 'PUT':
        return abort(403)
    else:
        return abort(405)