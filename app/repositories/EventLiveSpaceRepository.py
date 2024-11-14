from app.config import database
from app.models.EventLiveSpace import EventLiveSpace

def insert_event_live_space(createEventLiveSpaceData: EventLiveSpace):
    filterCriteria = {'_createdBy': createEventLiveSpaceData.createdBy}
    updateCriteria = {'$set': {
                        'eventId': createEventLiveSpaceData.eventId,
                        'createdAt': createEventLiveSpaceData.createdAt,
                        'channelId': createEventLiveSpaceData.channelId,
                        'photoUrl': createEventLiveSpaceData.photoUrl,
                        'chatroomId': createEventLiveSpaceData.chatroomId
                    }}
    return database.db["LiveStreamVideos"].update_one(filter=filterCriteria, update=updateCriteria, upsert=True)