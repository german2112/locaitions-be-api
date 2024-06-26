from fastapi import APIRouter, status, Query, Depends
from fastapi import APIRouter, Body
from app.models.JoinEventRequest import JoinEventRequest
from app.services import JoinEventRequestService as joinEventRequestService
from fastapi.responses import JSONResponse
from app.utils.ResponseUtils import *
from app.common.token_verification import verify_firebase_token
from typing import Optional

joinEventRequestRouter = APIRouter(prefix="/join-event-request")


@joinEventRequestRouter.post("", response_description="Inserted id")
def insert(payload: JoinEventRequest):
    try:
        response = joinEventRequestService.insert(payload)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=get_successful_response(response))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))


@joinEventRequestRouter.put("/{id}", response_description="")
def update(id: str, payload: JoinEventRequest):
    try:
        response = joinEventRequestService.update(id, payload)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(response))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))


@joinEventRequestRouter.get("")
def find(
        event_id: Optional[str] = Query(
            None, title="event_id", description="event id"),
        user_uid: Optional[str] = Query(
            None, title="user_uid", description="user uid"),
        join_status: Optional[str] = Query(
            None, title="status", description="status")):
    try:
        response = joinEventRequestService.find(event_id, user_uid, join_status)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(response))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))
