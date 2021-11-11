from pusher_push_notifications import PushNotifications

beams_client = PushNotifications(
    instance_id='ac1386a2-eac8-4f11-aaab-cad17174260a',
    secret_key='96C6F861EECA0E13EA1C5F08CDD2AAB09A3519E176312044ACCCF7AB87493263',
)

class PushNotifications:

    @staticmethod
    def winked_back(userID, title="Amāre"):
        """
        Sends a notification to the user that they were winked at t by someone.
        """
        message = f"🥳 They 😉 back at you. Make some magic happen 🪄."

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
                },
            },
        )

    @staticmethod
    def winked_at(userID,  title="Amāre"):
        """
        Sends a notification to the user that they were winked at  by someone.
        """
        message = f"Someone 😉 at you, what's your response 😏?"

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
                    }
                },
            },
        },
        )