from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from app.models.FavoriteEvent import FavoriteEvent
from app.services import FavoriteEventService as favoriteEventService
from app.utils.ResponseUtils import *
from fastapi.encoders import jsonable_encoder
from typing import Optional


favoriteEventRouter = APIRouter(prefix="/favorite_event")


@favoriteEventRouter.post("", tags=["Favorite Events"], description="Create a record of a favorite event")
def create(favoriteEvent: FavoriteEvent):
    try:
        response = favoriteEventService.create(favoriteEvent)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(jsonable_encoder(response)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))


@favoriteEventRouter.get("", tags=["Favorite Events"], description="Find favorite event with event id or user id")
def find(
    user_id: Optional[str] = Query(
        None, title="user_id", description="User id"),
    event_id: Optional[str] = Query(
        None, title="event_id", description="event id")
):
    try:
        response = favoriteEventService.find_by_user_and_event(
            user_id, event_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(jsonable_encoder(response)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))


@favoriteEventRouter.delete("", tags=["Favorite Events"], description="delete favorite event with event id or user id")
def delete(
    user_id: Optional[str] = Query(
        None, title="user_id", description="User id"),
    event_id: Optional[str] = Query(
        None, title="event_id", description="event id")
):
    try:
        response = favoriteEventService.delete_by_user_and_event(
            user_id=user_id, event_id=event_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(jsonable_encoder(response)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))


@favoriteEventRouter.get("/count/{event_id}",  tags=["Favorite Events"], description="count favorite events with event id")
def count(
    event_id: str
):
    try:
        response = favoriteEventService.count_by_event(event_id=event_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(jsonable_encoder(response)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))
