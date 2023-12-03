



class PushNotifications:

    @staticmethod
    def winked_back(userID, winker, title="Amāre"):
        from database.user import User
        """
        Sends a notification to the user that they were winked at t by someone.
        """

        person = User(id=winker)

        message = f"🥳 @{person.username} 😉 back at you. Make some magic happen 🪄."
        User.send_notification_to_user(userID, title, message)


        

    @staticmethod
    def winked_at(userID, winker,  title="Amāre"):
        from database.user import User
        """
        Sends a notification to the user that they were winked at  by someone.
        """
        person = User(id=winker)
        message = f"@{person.username} 😉 at you, what's your response 😏?"
        User.send_notification_to_user(userID, title, message)

       

    @staticmethod
    def send_friend_request_to(userID, requester_uid, title="Amāre"):
        from database.user import User
        """
        Send notification to user that they received a friend request
        """
        requester = User(id=requester_uid)
        message = f"@{requester.username} sent you a friend request ✉️. Know them?"
        User.send_notification_to_user(userID, title, message)

        

    @staticmethod
    def acceptFriendRequestFrom(requester_uid, requested_uid, title="Amāre"):
        from database.user import User
        """
        Sends a notification to the user (requester) that their friend request was accepted
        """
        requested = User(id=requested_uid)
        message = f"@{requested.username} accepted ✅ your friend request. 🥂"
        User.send_notification_to_user(requester_uid, title, message)

        
        


    @staticmethod
    def checked_out(userID, message="Someone is checking you out 👀, we won't say who though. 🤫", title="Amāre"):
        """
        Sends a notification to the user that they were checked out by someone.
        """
        from database.user import User
        User.send_notification_to_user(userID, title, message)
        
        