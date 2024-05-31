from app.config import database
from bson import ObjectId

from app.models.FavoriteEvent import FavoriteEvent


def create(payload: FavoriteEvent):
    return database.db["FavoriteEvents"].insert_one(payload)


def find_by_user_and_event(user_id: str, event_id: str):
    return database.db["FavoriteEvents"].find_one({"user_id": user_id, "event_id": event_id})


def delete_by_user_and_event(user_id: str, event_id: str):
    return database.db["FavoriteEvents"].delete_one({"user_id": user_id, "event_id": event_id})


def count_by_event(event_id):
    return database.db["FavoriteEvents"].count_documents({"event_id": event_id})
