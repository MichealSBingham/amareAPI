# pip install stream-chat
import stream_chat


STREAM_KEY = "6vb87hptvk7d"
STREAM_SECRET = "khx3uf4rtnyr23shme3u86dqe4m5veh8sn5zkhwuuypjd37jw4yh2dyn5xas7cy6"

server_client = stream_chat.StreamChat(api_key=STREAM_KEY, api_secret=STREAM_SECRET)



def get_token_from_user_id(user_id):
    """This returns a token that the frontend can use to authenticate with the backend to send messages. 
    This token is generated from the user_id and has no expiration date."""
    return server_client.create_token(user_id)



#TODO: Make a method to revoke the token when the user logs out.