#TODO: House overlays
def add_synastry_aspects_to_database(user1, user2):
    """ Adds all of the synastry aspects to the database for both users. TODO: Add comets and house overlays"""
    from database.user import db

    #Compute synastry both ways (with user1 as the inner chart and with user1 as the outer chart)

    syn1 = user1.synastry(user2)
    syn2 = user2.synastry(user1)
    a1 = syn1.toArray() #aspects with user1 as the inner
    a2 = syn2.toArray() #aspects with user2 as the inner


    db.collection('synastry').document(user1.id).collection("outerChart").document(user2.id).set({'aspects': a1})
    db.collection('synastry').document(user2.id).collection("outerChart").document(user1.id).set({'aspects': a2})

def delete_synastry_chart(user1_id, user2_id): 
    """ Delete user1's synastry chart from user2's charts. Deletes synastry/user2_id/outerChart/user1_id. Will not delete synastry/user1_id/outerChart/user2_id.. need to do this seperately. Deletes user2's chart.
    """


    pass 