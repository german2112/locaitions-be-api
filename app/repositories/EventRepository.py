from app.config import database
from typing import List
from bson import ObjectId

def filter_events(eventFilters):
    return database.db['Events'].find(eventFilters)

def insert_event(event):
    return database.db['Events'].insert_one(event)

def get_by_id(id: ObjectId):
    return database.db['Events'].find_one({'_id': id})

def update_event(eventId: ObjectId, photos: List[dict]):
    filterCriteria = {'_id':eventId}
    updateCriteria = {'$push': {'photos': {'$each': photos}}}
    return database.db['Events'].update_one(filter=filterCriteria, update=updateCriteria)