from database.user import db
from google.cloud.firestore_v1 import Increment


# Increments a new user for analytics to use
def new_user():
    db.collection('amare').document('app').set({"users": {"total": Increment(1)}}, merge=True)

def less_user():
    db.collection('amare').document('app').set({"users": {"total": Increment(-1)}}, merge=True)



def new_male():
    db.collection('amare').document('app').set({"users": {"males": Increment(1)}}, merge=True)

def less_male():
    db.collection('amare').document('app').set({"users": {"males": Increment(-1)}}, merge=True)


def new_female():
    db.collection('amare').document('app').set({"users": {"female": Increment(1)}}, merge=True)

def less_female():
    db.collection('amare').document('app').set({"users": {"female": Increment(-1)}}, merge=True)


def new_trans_male():
    db.collection('amare').document('app').set({"users": {"male_trans": Increment(1)}}, merge=True)

def less_trans_male():
    db.collection('amare').document('app').set({"users": {"male_trans": Increment(-1)}}, merge=True)


def new_trans_female():
    db.collection('amare').document('app').set({"users": {"female_trans": Increment(1)}}, merge=True)


def less_trans_female():
    db.collection('amare').document('app').set({"users": {"female_trans": Increment(-1)}}, merge=True)


def new_non_binary():
    db.collection('amare').document('app').set({"users": {"non_binary": Increment(1)}}, merge=True)


def less_non_binary():
    db.collection('amare').document('app').set({"users": {"non_binary": Increment(-1)}}, merge=True)

