from app.models.EventFilters import EventFiltersSchema
from app.models.Event import EventSchema
from app.repositories import EventRepository
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from app.exceptions.BadRequestException import BadRequestException
from app.exceptions.InternalServerError import InternalServerError
from typing import List
from app.exceptions.BadRequestException import BadRequestException
from zoneinfo import ZoneInfo
from app.helpers import EventHelper as eventHelper
from bson import ObjectId
from fastapi import UploadFile


def get_events_by_filter(event: EventFiltersSchema):
    filters = eventHelper.build_event_filters(event)
    event_list = []
    try:
        if ("tags" in filters and len(filters["tags"]) > 0):
            event_ids = eventHelper.get_event_ids_from_tags(filters["tags"])
            filters.pop("tags")
            filters = {
                **filters,
                "_id": {"$in": event_ids}
            }

        event_list = EventRepository.filter_events(filters)
        return eventHelper.format_list_of_events(eventList=event_list)
    except Exception as e:
        raise InternalServerError(str(e))


def create_event(event: EventSchema):
    if event.userId == "" and event.clubId == "":
        raise BadRequestException(
            "An event must have either userId or clubId but neither was given.")
    try:
        jsonEvent = jsonable_encoder(event)
        event_tags = jsonEvent.get("tags", [])
        jsonEvent.pop("tags")
        jsonEvent["createdDate"] = datetime.now(ZoneInfo('UTC'))
        createdEvent = EventRepository.insert_event(jsonEvent)
        if len(event_tags) > 0:
            eventHelper.insert_tags(event_tags, str(createdEvent.inserted_id))
    except Exception as e:
        raise InternalServerError(str(e))
    return str(createdEvent.inserted_id)


async def upload_event_photos(eventId: str, files: List[UploadFile], isProfile: bool):
    eventToUpdate = EventRepository.get_by_id(ObjectId(eventId))
    if not eventToUpdate:
        raise BadRequestException("No event found with the given eventId")
    formattedPhotosList = await eventHelper.get_formatted_photos(files, isProfile)
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
        photos=eventToUpdate["photos"]+formattedPhotosList,
        capacity=eventToUpdate["capacity"]).to_dict()
    updatedEvent = EventRepository.update_event(
        ObjectId(eventId), formattedPhotosList)
    if updatedEvent.matched_count > 0:
        return resultantEvent
    else:
        raise InternalServerError(
            f"Error while adding photos for event: {eventId}. Please try again.")


def find_by_id(event_id: str):
    try:
        found_event = EventRepository.get_by_id(ObjectId(event_id))
        if found_event != None:
            event_tags = eventHelper.get_labels_from_event_id(event_id)
            if found_event["clubId"] != None:
                found_place = eventHelper.get_event_place(
                    found_event["clubId"])
                found_event = {**found_event, "place": found_place}

        return {
            **found_event,
            "tags": event_tags,
            "_id": str(found_event["_id"]),
            "createdDate": str(found_event["createdDate"]),
            "photos": eventHelper.format_event_photos(found_event["photos"]) if "photos" in found_event else []
        }
    except Exception as e:
        raise InternalServerError(str(e))
