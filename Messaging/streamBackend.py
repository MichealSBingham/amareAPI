# streamBackend.py

from stream_chat import StreamChat

# Set up Stream Chat client
api_key = "92jyyxebed2m"
api_secret = "zh8xege9catts7pfdageqsfc6vhgwttqedrsa9kvfyxjmucqst4wn97ycgn765wc"
chat_region = "us-east"

chat_client = StreamChat(api_key, api_secret, region=chat_region)
dasha_image_url = "https://firebasestorage.googleapis.com/v0/b/findamare.appspot.com/o/0_1.png?alt=media&token=c4e66adc-9ba3-4acf-b6bd-f7e2ee167237"

# Create Dasha's user
def create_dasha_user():
    user_id = "dasha"
    profile_image = "https://firebasestorage.googleapis.com/v0/b/findamare.appspot.com/o/0_1.png?alt=media&token=c4e66adc-9ba3-4acf-b6bd-f7e2ee167237"

    try:
        chat_client.upsert_user({"id": user_id, "role": "admin", "image": dasha_image_url, "name": "Dasha"})

       

        print(f"User Dasha created")
    except Exception as e:
        print(f"Error creating Dasha's user: {e}")

# Send a welcome message to a specific user
def send_welcome_message(user_id):
    channel_type = "messaging"

    channel_id = f"{user_id}-dasha"

    try:
        

        channel = chat_client.channel(channel_type, channel_id)
        channel.create(user_id)
        channel.update({"name": "Dasha", "image": dasha_image_url})


        channel.add_members(["dasha", user_id]) #IF Necessary 

        
        # Send the welcome message
        message = {"text": "Hey, I'm Dasha! 💁🏼‍♀️ Ask me anything about your birth chart , astrology, relationships 💖 , and dating 👩🏼‍❤️‍💋‍👨🏾! I can also give readings-- only for you though! 😉"}
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
if __name__ == "__main__":
    create_dasha_user()

    # Replace 'example_user_id' with the actual user ID you want to send the welcome message to
    send_welcome_message("example_user_id")

    # Replace 'example_user_id' with the actual user ID you want to send a test message to
    send_message_to_user("example_user_id", "Hello there!")

"""