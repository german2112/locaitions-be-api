from app.models.EventFilters import EventFiltersSchema
from app.models.Event import EventSchema
from app.repositories import EventRepository
from app.utils.ImageUtils import upload_image_to_S3
from datetime import datetime, UTC
from fastapi.encoders import jsonable_encoder
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.InternalServerError import InternalServerError
from pymongo import CursorType
from typing import List
from fastapi import UploadFile
from app.factories.AwsFactory import create_aws_session
from app.models.Photo import PhotoSchema
from bson import ObjectId
from app.exceptions.BadRequestException import BadRequestException

def get_events_by_filter(event: EventFiltersSchema):
    filters = build_event_filters(event)
    try:
        eventList = EventRepository.filter_events(filters)
        return format_list_of_events(eventList)
    except Exception as e:
        raise InternalServerError(str(e))
    
def format_list_of_events(eventList: CursorType):
    formattedEventList = []
    for event in eventList:
        eventItem = {
            "id": str(event["_id"]),
            "name": event["name"],
            "location": event["location"],
            "rating": event["rating"],
            "status": event["status"],
            "type": event["type"],
            "description": event["description"],
            "userId": event["userId"],
            "clubId": event["clubId"],
            "startDate": event["startDate"],
            "endDate": event["endDate"],
            "createdDate": event["createdDate"] 
        }
        formattedEventList.append(eventItem)
    return formattedEventList


def build_event_filters(event: EventFiltersSchema):
    eventFilters = {}

    if(event.name):
        eventFilters["name"] = event.name
    if(event.date):
        eventFilters["date"] = event.date
    if(event.clubId):
        eventFilters["clubId"] = event.clubId
    if(event.type):
        eventFilters["type"] = event.type
    if(event.userId):
        eventFilters["userId"] = event.userId
    if(event.location):
        eventFilters["location"] = event.location.to_dict()
    if(event.status):
        eventFilters["status"] = event.status.value
    
    return eventFilters

def create_event(event: EventSchema):
    if event.userId == "" and event.clubId == "":
        raise BadRequestException("An event must have either userId or clubId but neither was given.")
    try:
        jsonEvent = jsonable_encoder(event)
        jsonEvent["createdDate"] = datetime.now(UTC)
        createdEvent = EventRepository.insert_event(jsonEvent)
    except Exception as e:
        raise InternalServerError(str(e))
    return str(createdEvent.inserted_id)

async def get_formatted_photos(files: List[UploadFile], isProfile: bool):
    try:
        session = create_aws_session()
        photoUrl = ''
        formattedPhotosList: List[dict] = []
        for file in files:
            photoUrl = await upload_image_to_S3(session, file)
            photo = PhotoSchema(filename=file.filename, 
                                fileUrl=photoUrl, 
                                createdAt=datetime.now(UTC), 
                                isProfile=isProfile)
            formattedPhotosList.append(photo.to_dict())
        return formattedPhotosList
    except Exception as e:
        raise InternalServerError(f"Error formatting new event photos. Error: {str(e)}")

async def upload_event_photos(eventId: str, files: List[UploadFile], isProfile: bool):
    eventToUpdate = EventRepository.get_by_id(ObjectId(eventId))
    if not eventToUpdate:
        raise BadRequestException("No event found with the given eventId")
    formattedPhotosList = await get_formatted_photos(files, isProfile)
    resultantEvent = EventSchema(
            _id=eventToUpdate["_id"],
            name=eventToUpdate["name"],
            location=eventToUpdate["location"],
            rating=eventToUpdate["rating"],
            createdDate=eventToUpdate["createdDate"],
            status=eventToUpdate["status"],
            type=eventToUpdate["type"],
            description=eventToUpdate["description"],
            userId=eventToUpdate["userId"],
            clubId=eventToUpdate["clubId"],
            startDate=eventToUpdate["startDate"],
            endDate=eventToUpdate["endDate"],
            photos=eventToUpdate["photos"]+formattedPhotosList).to_dict()
    updatedEvent = EventRepository.update_event(ObjectId(eventId), formattedPhotosList)
    if updatedEvent.matched_count > 0:
        return resultantEvent
    else:
        raise InternalServerError(f"Error while adding photos for event: {eventId}. Please try again.")
        
        