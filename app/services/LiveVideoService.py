from app.models.User import UserSchema
from app.models.Event import EventSchema
from pydantic import ValidationError
from app.repositories import LiveVideoRepository
from app.exceptions.InternalServerError import InternalServerError
from app.exceptions.BadRequestException import BadRequestException
from app.models.LiveStreamVideo import LiveStreamVideoSchema
from app.repositories.PlaceRepository import get_by_id
import app.repositories.EventRepository as EventRepository
from app.dto.CreateLiveSpaceDTO import CreateLiveSpaceDTO
from bson.objectid import ObjectId
from datetime import datetime, UTC

def validate_if_user_in_area(user: UserSchema, event: EventSchema):
    userCoordinates = (user.location["lng"], user.location["lat"])
    coordinatesThatIntersectsWithUser = list(LiveVideoRepository.validate_if_user_in_area(userCoordinates, ObjectId(event.uid)))
    return "False" if len(coordinatesThatIntersectsWithUser) == 0 else "True"

def get_event_owner_stream(eventId: str, eventCreatedBy: str):
    try:
        event: EventSchema = EventRepository.get_by_id(ObjectId(eventId))
        if not event:
            raise BadRequestException(f"No event found with the given eventId: {eventId}")
        eventOwnerFormattedStream = {}
        eventCreatedBy = ""
        if(event['type'] == "Club"): #Gets the owner of the organizer club to validate if it is live streaming
            placeOwnerOfEvent = get_by_id(ObjectId(event['clubId']))
            if placeOwnerOfEvent == None:
                raise BadRequestException(f"The event was created by inexistent club: {event['clubId']}.")
            eventCreatedBy = placeOwnerOfEvent["ownerId"]
        else:
            eventCreatedBy = event['userId']
        eventOwnerStream = LiveVideoRepository.get_event_owner_stream(str(event['_id']), eventCreatedBy)
        if(eventOwnerStream != None):
            eventOwnerFormattedStream = LiveStreamVideoSchema(id=str(eventOwnerStream["_id"]), 
                                                            eventId=eventOwnerStream["eventId"], 
                                                            createdBy=eventOwnerStream["createdBy"],
                                                            channelId=eventOwnerStream["channelId"]).to_dict()
        return eventOwnerFormattedStream
    except ValidationError as e:
        raise InternalServerError(f'Validation error when creating Live stream object. Error: {str(e)}')
    except Exception as e:
        raise InternalServerError(f'Error while retrieving live stream of owner: {eventCreatedBy} for event {event._id}. Error: {e}')
    
def create_live_stream(liveStreamData: CreateLiveSpaceDTO):
    try:
        createdLiveStream = LiveStreamVideoSchema(createdBy=liveStreamData.createdBy, eventId=liveStreamData.eventId, channelId=liveStreamData.username, createdAt=str(datetime.now(UTC)), photoUrl=liveStreamData.photoUrl)
        LiveVideoRepository.insert_live_stream_video(createdLiveStream)
        return createdLiveStream.to_dict()
    except Exception as e:
        raise InternalServerError(f"Error while creating live stream video. Error: {str(e)}")