from app.config import database

def find_by_phone(phone: str):
    return database.db["Users"].find_one({"phone": phone})

def find_by_email(email: str):
    return database.db["Users"].find_one({"email": email})

def find_by_id(uid: str):
    return database.db["Users"].find_one({"uid": uid})

def find_by_userName(userName: str):
    return database.db["Users"].find_one({'userName': userName})

def insert_user(user):
    return database.db["Users"].insert_one(user)

def update_user(uid, user):
    return database.db["Users"].update_one({'uid': uid}, {'$set': user})