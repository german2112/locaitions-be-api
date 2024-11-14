from app.config import database
from bson.objectid import ObjectId
import pymongo

def upload_photo(photo):
    return database.db["Photos"].insert_one(photo)

def upload_profile_photo(photo):
    database.db["Photos"].delete_one({"userUid": photo['userUid'], "isProfile": True})
    return database.db["Photos"].insert_one(photo)

def find_by_user_uid(uid: str):
    return database.db["Photos"].find({"userUid": uid}).sort('_id', pymongo.DESCENDING)

def delete_by_id(id: str):
    return database.db['Photos'].delete_one({'_id': ObjectId(id)})