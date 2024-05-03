from app.config import database
from app.models.LiveStreamVideo import LiveStreamVideoSchema

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

def insert_live_stream_video(createLiveStreamData: LiveStreamVideoSchema):
    filterCriteria = {'_createdBy': createLiveStreamData.createdBy}
    updateCriteria = {'$set': {
                        'eventId': createLiveStreamData.eventId,
                        'createdAt': createLiveStreamData.createdAt,
                        'channelId': createLiveStreamData.channelId
                    }}
    return database.db["LiveStreamVideos"].update_one(filter=filterCriteria, update=updateCriteria, upsert=True)