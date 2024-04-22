from app.config import database

def validate_if_user_in_area(userCoordinates, eventId):
    database.db["Events"].create_index([("area", "2dsphere")])

    return database.db["Events"].find({
        '_id': eventId,
        'area': {
            '$geoIntersects': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': userCoordinates
                }
            }
        }
    })

def get_event_owner_stream(eventId: str, eventCreatedBy: str):
    return database.db["LiveStreamVideos"].find_one(filter={
        "eventId": eventId,
        "createdBy": eventCreatedBy
    })