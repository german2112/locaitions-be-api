from app.repositories import TagRepository as tagRepository
from bson import ObjectId
from typing import List
from pymongo import CursorType
from app.models.EventFilters import EventFiltersSchema
import re
from app.repositories import TagRepository as tagRepository
from app.models.Photo import PhotoSchema
from app.factories.AwsFactory import create_aws_session
from app.utils.ImageUtils import upload_image_to_S3
from fastapi import UploadFile
from app.exceptions.InternalServerError import InternalServerError
from datetime import datetime
from zoneinfo import ZoneInfo
from app.repositories import PlaceRepository as placeRepository


def get_event_ids_from_tags(tags: List[str]):
    found_events = tagRepository.find_distinct(
        "event_id", {"label": {"$in": tags}})
    return [ObjectId(event_id) for event_id in found_events]


def get_labels_from_event_id(eventId: str):
    found_labels = tagRepository.find_distinct("label", {"event_id": eventId})
    return found_labels


def format_list_of_events(eventList: CursorType):
    formattedEventList = []
    for event in eventList:
        event_id = str(event["_id"])
        event_tags = get_labels_from_event_id(eventId=event_id)
        eventItem = {
            "_id": event_id,
            "name": event["name"],
            "status": event["status"],
            "type": event["type"],
            "description": event["description"],
            "userId": event["userId"],
            "clubId": event["clubId"],
            "startDate": event["startDate"],
            "endDate": event["endDate"],
            "createdDate": str(event["createdDate"]),
            "tags": event_tags,
            "capacity": event["capacity"] if "capacity" in event else 0,
            "photos": format_event_photos(event["photos"]) if "photos" in event else []
        }
        formattedEventList.append(eventItem)
    return formattedEventList


def build_event_filters(event: EventFiltersSchema):
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


def insert_tags(tags: List[str], event_id: str):
    tags_to_be_created = []
    for tag in tags:
        tag_item = {
            "label": re.sub(r'[^a-zA-Z0-9]', '', tag),
            "event_id": event_id
        }
        tags_to_be_created.append(tag_item)

    return tagRepository.insert_many(tags_to_be_created)


async def get_formatted_photos(files: List[UploadFile], isProfile: bool):
    try:
        session = create_aws_session()
        photoUrl = ''
        formattedPhotosList: List[dict] = []
        for file in files:
            photoUrl = await upload_image_to_S3(session, file)
            photo = PhotoSchema(filename=file.filename,
                                fileUrl=photoUrl,
                                createdAt=datetime.now(ZoneInfo('UTC')),
                                isProfile=isProfile)
            formattedPhotosList.append(photo.to_dict())
        return formattedPhotosList
    except Exception as e:
        raise InternalServerError(
            f"Error formatting new event photos. Error: {str(e)}")


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
