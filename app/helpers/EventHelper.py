from app.repositories import TagRepository as tagRepository
from bson import ObjectId
from typing import List
from pymongo import CursorType
from app.schemas.EventFilter import EventFilter
from app.models.Tag import TagSchema
import re
from app.repositories import TagRepository as tagRepository
from app.factories.EventFactory import EventFactory
from datetime import datetime
from app.repositories import PlaceRepository as placeRepository

def get_labels_from_event_id(eventId: str):
    found_labels = tagRepository.find_distinct("label", {"event_id": eventId})
    return found_labels


def format_list_of_events(eventList: CursorType):
    formattedEventList = []
    for event in eventList:
        eventItem = EventFactory.create_event(event)
        formattedEventList.append(eventItem.to_dict())
    return formattedEventList


def build_event_filters(event: EventFilter):
    eventFilters = {}

    if (event.name):
        eventFilters["name"] = {
            '$regex': event.name,
            '$options': 'i'
        }
    if (event.startDate):
        incoming_date = datetime.strptime(event.startDate, "%d/%m/%Y")
        formatted_date = incoming_date.strftime("%Y-%m-%d %H:%M")
        eventFilters["startDate"] = {"$gte": formatted_date}
    if (event.clubId):
        eventFilters["clubId"] = event.clubId
    if (event.type):
        eventFilters["type"] = event.type
    if (event.userId):
        eventFilters["userId"] = event.userId
    if (event.location):
        eventFilters["location"] = event.location.to_dict()
    if (event.status):
        eventFilters["status"] = event.status.value
    if (event.tags):
        eventFilters["tags"] = event.tags

    return eventFilters


def insert_tags(tags: List[TagSchema], event_id: str):
    tags_to_be_created = []
    for tag in tags:
        tag['label'] = re.sub(r'[^a-zA-Z0-9]', '', tag['label'])
        tag['event_id'] = event_id
        tags_to_be_created.append(tag)

    return tagRepository.insert_many(tags_to_be_created)

def get_event_place(placeId: str):
    found_place = placeRepository.get_by_id(ObjectId(placeId))
    if (found_place != None):
        found_place = {**found_place, "_id": str(found_place["_id"])}
    return found_place


def format_event_photos(photos) -> List:
    formatted_photos = []
    for photo in photos:
        formatted_photos.append({
            **photo,
            "createdAt": str(photo["createdAt"])
        })
    return formatted_photos
