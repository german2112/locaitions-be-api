from app.config import database
from bson import ObjectId

def get(placeFilters):
    return database.db["Clubs"].aggregate([
        {
            "$addFields": {
                "clubId": {
                    "$toString": "$_id"
                }  
            }
        },
        {
            "$match": placeFilters
        },
        {
            "$lookup": {
            "from": "PlacePhotos",
            "localField": "clubId",
            "foreignField": "placeId",
            "as": "placePhotos"
            }
        }
    ])

def get_by_id(id: ObjectId):
    return database.db['Clubs'].find_one({'_id': id})