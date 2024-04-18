from app.models.EventFilters import EventFiltersSchema
from app.models.Event import EventSchema
from app.repositories import EventRepository
from bson.objectid import ObjectId
from datetime import datetime, UTC
from fastapi.encoders import jsonable_encoder
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.InternalServerError import InternalServerError
from pymongo import CursorType

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
        eventFilters["clubId"] = ObjectId(event.clubId)
    if(event.type):
        eventFilters["type"] = event.type
    if(event.userId):
        eventFilters["userId"] = event.userId
    if(event.location):
        eventFilters["location"] = event.location
    if(event.status):
        eventFilters["status"] = event.status
    
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