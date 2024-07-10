from app.config import database
from bson import ObjectId

def filter_places(placeFilters):
    return database.db["Clubs"].find(placeFilters)

def get_by_id(id: ObjectId):
    return database.db['Clubs'].find_one({'_id': id})