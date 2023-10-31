from pusher_push_notifications import PushNotifications

beams_client = PushNotifications(
    instance_id='ac1386a2-eac8-4f11-aaab-cad17174260a',
    secret_key='96C6F861EECA0E13EA1C5F08CDD2AAB09A3519E176312044ACCCF7AB87493263',
)

class PushNotifications:

    @staticmethod
    def winked_back(userID, winker, title="Amāre"):
        from database.user import User
        """
        Sends a notification to the user that they were winked at t by someone.
        """

        person = User(id=winker)

        message = f"🥳 @{person.username} 😉 back at you. Make some magic happen 🪄."

        response = beams_client.publish_to_interests(
            interests=[userID],
            publish_body={
                'apns': {
                    'aps': {
                        'alert': {
                            "title": title,
                            "body": message
                        }
                    },
                    'winked': userID,
                    'winker': winker
                },
            },
        )

    @staticmethod
    def winked_at(userID, winker,  title="Amāre"):
        from database.user import User
        """
        Sends a notification to the user that they were winked at  by someone.
        """
        person = User(id=winker)
        message = f"@{person.username} 😉 at you, what's your response 😏?"

        response = beams_client.publish_to_interests(
            interests=[userID],
            publish_body={
                'apns': {
                    'aps': {
                        'alert': {
                            "title": title,
                            "body": message
                        }
                    },
                    'winked': userID,
                    'winker': winker
                },
            },
        )

    @staticmethod
    def send_friend_request_to(receiver_id, sender_id, sender_username, title="Amāre"):
        from database.user import User
        """
        Send notification to user that they received a friend request
        """
        
        message = f"@{sender_username} sent you a friend request ✉️. Know them?"

        response = beams_client.publish_to_interests(
            interests=[receiver_id],
            publish_body={
                'apns': {
                    'aps': {
                        'alert': {
                            "title": title,
                            "body": message
                        }
                    },
                    'requester': sender_id
                },
            },
        )

    @staticmethod
    def acceptFriendRequestFrom(sender_uid, receiver_uid, receiver_username, title="Amāre"):
        from database.user import User
        """
        Sends a notification to the user (requester) that their friend request was accepted
        """
        
        message = f"@{receiver_username} accepted ✅ your friend request. 🥂"

        response = beams_client.publish_to_interests(
            interests=[sender_uid],
            publish_body={
                'apns': {
                    'aps': {
                        'alert': {
                            "title": title,
                            "body": message
                        }
                    },
                    'requester': sender_uid,
                    'requested': receiver_uid
                },
            },
        )


    @staticmethod
    def checked_out(userID, message="Someone is checking you out 👀, we won't say who though. 🤫", title="Amāre"):
        """
        Sends a notification to the user that they were checked out by someone.
        """
        response = beams_client.publish_to_interests(
        interests=[userID],
        publish_body={
            'apns': {
                'aps': {
                    'alert': {
                        "title": title,
                        "body": message

                    },
                    'checked': userID
                },
            },
        },
        )