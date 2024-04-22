from app.models.User import UserSchema
from app.models.Event import EventSchema
from pydantic import ValidationError
from app.repositories import LiveVideoRepository
from app.exceptions.InternalServerError import InternalServerError
from app.models.LiveStreamVideo import LiveStreamVideoSchema
from bson.objectid import ObjectId

def validate_if_user_in_area(user: UserSchema, event: EventSchema):
    userCoordinates = (user.location["lng"], user.location["lat"])
    coordinatesThatIntersectsWithUser = list(LiveVideoRepository.validate_if_user_in_area(userCoordinates, ObjectId(event.uid)))
    return "False" if len(coordinatesThatIntersectsWithUser) == 0 else "True"

def get_event_owner_stream(eventId: str, eventCreatedBy: str):
    try:
        eventOwnerFormattedStream = {}
        eventOwnerStream = LiveVideoRepository.get_event_owner_stream(eventId, eventCreatedBy)
        if(eventOwnerStream != None):
            eventOwnerFormattedStream = LiveStreamVideoSchema(id=str(eventOwnerStream["_id"]), 
                                                            eventId=eventOwnerStream["eventId"], 
                                                            createdBy=eventOwnerStream["createdBy"],
                                                            channelId=eventOwnerStream["channelId"]).to_dict()
        return eventOwnerFormattedStream
    except ValidationError as e:
        raise InternalServerError(f'Validation error when creating Live stream object. Error: {str(e)}')
    except Exception as e:
        raise InternalServerError(f'Error while retrieving live stream of owner: {eventCreatedBy} for event {eventId}. Error: {e}')