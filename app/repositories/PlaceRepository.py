from app.config import database

def get():
    return database.db["Clubs"].aggregate([
        {
            "$addFields": {
                "clubId": {
                    "$toString": "$_id"
                }  
            }
        },
        {
            "$lookup": {
            "from": "PlacePhotos",
            "localField": "clubId",
            "foreignField": "placeId",
            "as": "placePhotos"
        }}
    ])