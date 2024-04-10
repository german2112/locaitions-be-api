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