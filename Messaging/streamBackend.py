# streamBackend.py

from stream_chat import StreamChat
import json 
import time
#import socketio

# Set up Stream Chat client
api_key = "92jyyxebed2m"
api_secret = "zh8xege9catts7pfdageqsfc6vhgwttqedrsa9kvfyxjmucqst4wn97ycgn765wc"
chat_region = "us-east"

chat_client = StreamChat(api_key, api_secret, region=chat_region)
dasha_image_url = "https://firebasestorage.googleapis.com/v0/b/findamare.appspot.com/o/0_1.png?alt=media&token=c4e66adc-9ba3-4acf-b6bd-f7e2ee167237"

def generate_admin_token():
    admin_user_id = "dasha"  # Replace with your desired admin user ID
    admin_token = chat_client.create_token(admin_user_id)
    return admin_token

token = generate_admin_token()


# Create Dasha's user
def create_dasha_user():
    user_id = "dasha"
    profile_image = "https://firebasestorage.googleapis.com/v0/b/findamare.appspot.com/o/0_1.png?alt=media&token=c4e66adc-9ba3-4acf-b6bd-f7e2ee167237"

    try:
        chat_client.upsert_user({"id": user_id, "role": "admin", "image": dasha_image_url, "name": "Dasha"})

       

        print(f"User Dasha created")
    except Exception as e:
        print(f"Error creating Dasha's user: {e}")

# Message handler function
def handle_message(event):
    # Extract relevant information from the event
    message = event["message"]
    sender_user_id = message.get("user", {}).get("id", "Unknown User")

    # Process the message (add your processing logic here)
    print(f"Received message from {sender_user_id}: {message['text']}")

    # Send a response back (for demonstration purposes)
    response_text = "Thanks for your message!"
    send_message_to_user(sender_user_id, response_text)


# Send a welcome message to a specific user
def send_welcome_message(user_id, message="Hey, I'm Dasha! 💁🏼‍♀️ Ask me anything about your birth chart , astrology, relationships 💖 , and dating 👩🏼‍❤️‍💋‍👨🏾! I can also give readings-- only for you though! 😉"):
    channel_type = "messaging"

    channel_id = f"{user_id}-dasha"

    try:
        

        channel = chat_client.channel(channel_type, channel_id)
        channel.create(user_id)
        channel.update({"name": "Dasha", "image": dasha_image_url})


        channel.add_members(["dasha", user_id]) #IF Necessary 

        
        # Send the welcome message
        message = {"text": message}
        channel.send_message(message, "dasha")
        print(f"Welcome message sent to user {user_id}.")
    except Exception as e:
        print(f"Error sending welcome message: {e}")

# Send a message to a specific user
def send_message_to_user(user_id, message_text):
    channel_type = "messaging"
    channel_id = f"{user_id}-dasha"

    try:
   
        channel = chat_client.channel(channel_type, channel_id)
        
        
        # Send the message
        message = {
    "text": message_text,
            }

        channel.send_message(message, "dasha")

        print(f"Message sent to user {user_id}: {message_text}")
    except Exception as e:
        print(f"Error sending message to user {user_id}: {e}")

"""

# Message handler function
def handle_message(event):
    # Extract relevant information from the event
    message = event["message"]
    sender_user_id = message.get("user", {}).get("id", "Unknown User")

    # Process the message (add your processing logic here)
    print(f"Received message from {sender_user_id}: {message['text']}")

    # Send a response back (for demonstration purposes)
    response_text = "Thanks for your message!"
    send_message_to_user(sender_user_id, response_text)

# Subscribe to message events for a specific channel
def subscribe_to_channel(user_id):
    channel_type = "messaging"
    channel_id = f"{user_id}-dasha"

    # Create a channel instance
    channel = chat_client.channel(channel_type, channel_id)

    # Add the message handler
    channel.add_listener(handle_message)

    # Watch the channel for new messages
    channel.watch()





# Manual testing function
def simulate_user_creation_and_message(userID):
    # Simulate a new user creation event
    user_id = "userID"
    pubsub_message = {'user_id': user_id}

    # Simulate calling the message handler
    handle_message({'text': 'Test message'}, {'data': json.dumps(pubsub_message)})

# Message handler function
def handle_message(event, context):
    # Extract relevant information from the Pub/Sub message
    pubsub_message = json.loads(context['data'].decode('utf-8'))
    user_id = pubsub_message.get('user_id', 'unknown_user')

    # Set up and watch the channel for new messages
    channel_type = "messaging"
    channel_id = f"{user_id}-dasha"

    # Create a channel instance
    channel = chat_client.channel(channel_type, channel_id)

    # Process the message (add your processing logic here)
    print(f"Received message for user {user_id}: {event['text']}")

    # Send a response back (for demonstration purposes)
    response_text = "Thanks for your message!"
    channel.send_message({"text": response_text}, "dasha")

if __name__ == "__main__":
    while True:
        simulate_user_creation_and_message()
        time.sleep(5)  # Simulate a delay between messages for testing


"""

testUser1 = "2V2mJdDLt7Q5fVUl8O8PtQv3tQN2"
testUser2 = "ZH17wkDgkIVFqQ2F9wtwcRPi5oo1"



# Assuming chat_client is already defined and authenticated
# chat_client = ...

testID = "!members-bdRFBY75-BL-SIErP2Ekytk5XT2EPpxDkEJgTCr0-Wk"

"""



def listen_to_channel_id(channel_id):
    
    
    channel_type = "messaging"
    print(f"Listening to channel id: {channel_id}")

    channel = chat_client.channel(channel_type, channel_id)

    sio = socketio.Client()

    @sio.on(f"message.new.{channel_id}")
    def on_new_message(data):
        user_sending_message = data.get('user', {}).get('id', '')
        message_text = data.get('text', '')

        # Process the message (add your processing logic here)
        print(f"Received message from user {user_sending_message}: {exitmessage_text}")

        # Send a response back
        response_text = "Thanks for your message!"
        #channel.send_message({"text": response_text}, user_id="dasha")
        #print(f"Sent response to user {user_sending_message}: {response_text}")

    # Authenticate "dasha"
    #dasha_token = token # chat_client.create_token("dasha")
   # chat_client.connect_user({"id": "dasha"}, dasha_token)
    chat_client.upsert_user({"id": "dasha", "role": "admin", "image": dasha_image_url, "name": "Dasha"})

    # Connect to Stream Chat WebSocket
    sio.connect(chat_client.base_url.replace('https', 'wss'))

    # Event handling loop
    sio.wait()



    # Set up the channel for an existing user
    userList = [user1id, user2id]
    userList.sort()
    idstring = '-'.join(userList)

    channel_id = f"!members-{idstring}"
    channel_type = "messaging"
    print(f"Listening to channel id: {channel_id}")

    channel = chat_client.channel(channel_type, channel_id)

    sio = socketio.Client()

    @sio.on("message.new")
    def on_new_message(data):
        user_sending_message = data.get('user', {}).get('id', '')
        message_text = data.get('text', '')

        # Process the message (add your processing logic here)
        print(f"Received message from user {user_sending_message}: {message_text}")

        # Send a response back
        response_text = "Thanks for your message!"
        channel.send_message({"text": response_text}, user_id="dasha")
        print(f"Sent response to user {user_sending_message}: {response_text}")

    # Connect to Stream Chat WebSocket
    sio.connect(chat_client.base_url.replace('https', 'wss'))
    sio.emit('join', {'user_id': user_id, 'type': 'user'})

    # Event handling loop
    sio.wait()

    
    #chat_client.set_user({"id": "dasha"}, token)

    # Authenticate the user
    #chat_client.update_user({"id": user1id})

    # Connect to the channel using WebSocket
    #channel.watch({"user_id": user1id})
    #channel.watch()

    # Event handling loop
    
    while True:
        event = chat_client.listen()
        
        if event["type"] == "message.new":
            message = event["message"]
            user_sending_message = message.get('user', {}).get('id', '')
            message_text = message.get('text', '')

            # Process the message (add your processing logic here)
            print(f"Received message from user {user_sending_message}: {message_text}")

            # Send a response back
            #response_text = "Thanks for your message!"
            #channel.send_message({"text": response_text}, "dasha")
           # print(f"Sent response to user {user_sending_message}: {response_text}")

    



# Function to listen for messages in an existing channel
def listen_to_channel(user_id):
    # Set up the channel for an existing user
    channel_type = "messaging"
    channel_id = f"{user_id}-dasha"
    channel = chat_client.channel(channel_type, channel_id)

    # Authenticate the user
    chat_client.update_user({"id": user_id})

    # Connect to the channel using WebSocket
    channel.watch({"user_id": user_id})

    # Event handling loop
    while True:
        event = chat_client.get_ws_event()

        if event["type"] == "message.new":
            message = event["message"]
            user_sending_message = message.get('user', {}).get('id', '')
            message_text = message.get('text', '')

            # Process the message (add your processing logic here)
            print(f"Received message from user {user_sending_message}: {message_text}")

            # Send a response back
            response_text = "Thanks for your message!"
            channel.send_message({"text": response_text}, "dasha")
            print(f"Sent response to user {user_sending_message}: {response_text}")

# Uncomment the following lines if you want to run this locally
# if __name__ == "__main__":
#     listen_to_channel("existing_user_id")


"""