


def index_friend_placements(user1, user2):
    """
    Indexes astrological placements of user1 under user2's 'myFriends' in Firestore.
    
    Structure:
    users/
        user2_id/
            myFriends_index/
                planet_name/
                    sign/
                        user1_id (additional fields)
                    
    Parameters:
    user1: User object to be indexed.
    user2: User object under whose 'myFriends' the indexing occurs.
    """
    from astrology.NatalChart import planetToDict
    from database.user import db 

    for planet in user1.planets():
        planet_name = planet.id
        planet_data = planetToDict(planet)
        sign = planet_data['sign']
        house = planet_data.get('house', None)

        data = {
            'is_on_cusp': planet_data['is_on_cusp'],
            'angle': planet_data['angle'],
            'is_retrograde': planet_data['is_retrograde'],
            'is_notable': user1.is_notable,
            'profile_image_url': user1.profile_image_url,
            'name': user1.name
        }

        # Index placement by sign
        db.collection('users').document(user2.id).collection('myFriends_index').document(planet_name).collection(sign).document(user1.id).set(data)

        # Index placement by house if available
        if house is not None:
            data['house'] = house
            db.collection('users').document(user2.id).collection('myFriends_index').document(planet_name).collection(f'House{house}').document(user1.id).set(data)


def delete_indexed_placements(user1, user2):
    """
    Deletes indexed astrological placements of user1 under user2's 'myFriends_index' in Firestore.
    The structure is as follows:
    users/user2_id/myFriends_index/planet_name/sign/user1_id

    Args:
        user1 (User): User object whose placements are to be deleted.
        user2 (User): User object under whose 'myFriends_index' the deletions occur.
    """
    
    from astrology.NatalChart import planetToDict
    from database.user import db 

    for planet in user1.planets():
        planet_name = planet.id
        planet_data = planetToDict(planet)
        sign = planet_data['sign']
        house = planet_data.get('house', None)

        # Delete indexed placement by sign
        db.collection('users').document(user2.id).collection('myFriends_index').document(planet_name).collection(sign).document(user1.id).delete()

        # Delete indexed placement by house if available
        if house is not None:
            db.collection('users').document(user2.id).collection('myFriends_index').document(planet_name).collection(f'House{house}').document(user1.id).delete()
