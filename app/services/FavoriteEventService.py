from app.repositories import FavoriteEventRepository as favoriteEventRepository
from app.models.FavoriteEvent import FavoriteEvent
from app.exceptions.InternalServerError import InternalServerError
from fastapi.encoders import jsonable_encoder


def create(payload: FavoriteEvent):
    try:
        found_favorite = find_by_user_and_event(
            payload.user_id, payload.event_id)
        if ("_id" in found_favorite):
            return str(found_favorite["_id"])

        payload = jsonable_encoder(payload)

        created_favorite_id = str(favoriteEventRepository.create(
            payload).inserted_id)

        return created_favorite_id
    except Exception as e:
        raise InternalServerError(str(e))


def find_by_user_and_event(user_id: str, event_id: str):
    try:
        favorite_event = favoriteEventRepository.find_by_user_and_event(
            user_id, event_id)
        return {**favorite_event, "_id": str(favorite_event["_id"])} if favorite_event is not None else {}
    except Exception as e:
        raise InternalServerError(str(e))


def delete_by_user_and_event(user_id: str, event_id: str):
    try:
        favoriteEventRepository.delete_by_user_and_event(user_id, event_id)
        return event_id
    except Exception as e:
        raise InternalServerError(str(e))


def count_by_event(event_id: str):
    try:
        return favoriteEventRepository.count_by_event(event_id)
    except Exception as e:
        raise InternalServerError(str(e))
