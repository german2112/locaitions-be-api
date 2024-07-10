from app.config import database
from typing import List
from bson import ObjectId


def filter_events(eventFilters):
    return database.db['Events'].aggregate([
        {
            "$addFields": {
                "eventId": {
                    "$toString": "$_id"
                }
            }
        },
        {
            "$match": eventFilters
        },
        {
            "$lookup": {
                "from": "Tags",
                "localField": "eventId",
                "foreignField": "event_id",
                "as": "eventTags"
            }
        }
    ])

def insert_event(event):
    return database.db['Events'].insert_one(event)

def get_by_id(id: ObjectId):
    return database.db['Events'].aggregate([
        {
            "$addFields": {
                "eventId": {
                    "$toString": "$_id"
                }
            }
        },
        {
            "$match": {"_id": id}
        },
        {
            "$lookup": {
                "from": "Tags",
                "localField": "eventId",
                "foreignField": "event_id",
                "as": "eventTags"
            }
        }
    ])

def update_event_photos(eventId: ObjectId, photos: List[dict]):
    filterCriteria = {'_id':eventId}
    updateCriteria = {'$push': {'photos': {'$each': photos}}}
    return database.db['Events'].update_one(filter=filterCriteria, update=updateCriteria)

def get_place_event(placeId:str, longitude: float, lattitude: float, status: str):
    filterCriteria = {
        "clubId": placeId,
        "location.mainCoordinates.coordinates": [longitude, lattitude],
        "status": status
    }
    return database.db['Events'].aggregate([
        {
            "$addFields": {
                "eventId": {
                    "$toString": "$_id"
                }
            }
        },
        {
            "$match": filterCriteria
        },
        {
            "$lookup": {
                "from": "Tags",
                "localField": "eventId",
                "foreignField": "event_id",
                "as": "eventTags"
            }
        }
    ])
