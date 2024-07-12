from app.schemas.EventFilter import EventFilter
from app.schemas.CreateEvent import CreateEvent
from app.factories.EventFactory import EventFactory
from app.repositories import EventRepository
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.InternalServerError import InternalServerError
from typing import List
from fastapi import UploadFile
from bson import ObjectId
from app.exceptions.BadRequestException import BadRequestException
from app.helpers.PhotoHelper import format_photos_to_insert
from app.helpers.EventHelper import build_event_filters, get_labels_from_event_id, get_event_place, format_event_photos, format_list_of_events, insert_tags
from zoneinfo import ZoneInfo

def get_events_by_filter(event: EventFilter):
    filters = build_event_filters(event)
    eventList = []
    try:
        eventList = EventRepository.filter_events(filters)
        return format_list_of_events(eventList=eventList)
    except Exception as e:
        raise InternalServerError(str(e))

def create_event(event: CreateEvent):
    if event.userId == "" and event.clubId == "":
        raise BadRequestException(
            "An event must have either userId or clubId but neither was given.")
    try:
        jsonEvent = jsonable_encoder(event)
        eventTags = jsonEvent.get("tags", [])
        jsonEvent.pop("tags")
        jsonEvent["photos"] = []
        jsonEvent["createdDate"] = str(datetime.now(ZoneInfo('UTC')))
        jsonEvent["rating"] = 5.0
        jsonEvent["chatroomId"] = '' #TODO implement logic for creating a chatroom when an event is created
        createdEvent = EventRepository.insert_event(jsonEvent)
        if len(eventTags) > 0:
            insert_tags(eventTags, str(createdEvent.inserted_id))
    except Exception as e:
        raise InternalServerError(str(e))
    return str(createdEvent.inserted_id)


async def upload_event_photos(eventId: str, files: List[UploadFile], isProfile: bool):
    foundEventCursor = EventRepository.get_by_id(ObjectId(eventId))
    if foundEventCursor._has_next():
        foundEvent = foundEventCursor.next()
        formattedPhotosList = await format_photos_to_insert(files, isProfile)
        resultantEvent = EventFactory.create_event(foundEvent).to_dict()
        resultantEvent["photos"] = resultantEvent["photos"] + formattedPhotosList
        updatedEvent = EventRepository.update_event_photos(ObjectId(eventId), formattedPhotosList)
        if updatedEvent.matched_count > 0:
            return resultantEvent
        else:
            raise InternalServerError(
                f"Error while adding photos for event: {eventId}. Please try again.")
    raise BadRequestException("No event found with the given eventId")

def find_by_id(event_id: str):
    try:
        foundEventCursor = EventRepository.get_by_id(ObjectId(event_id))
        if foundEventCursor._has_next():
            foundEvent = foundEventCursor.next()
            if foundEvent["clubId"] != None:
                found_place = get_event_place(
                    foundEvent["clubId"])
                foundEvent = {**foundEvent, "place": found_place}
            return EventFactory.create_event(foundEvent).to_dict()
    except Exception as e:
        raise InternalServerError(str(e))
