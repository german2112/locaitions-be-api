from app.config import database

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