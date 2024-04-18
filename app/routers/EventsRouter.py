from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from app.models.EventFilters import EventFiltersSchema
from app.models.Event import EventSchema
from fastapi.encoders import jsonable_encoder
from app.services import EventService as eventService
from app.common.token_verification import verify_firebase_token
from app.utils.ResponseUtils import *

eventsRouter = APIRouter(prefix="/events")

@eventsRouter.post("/filter-event")
def find_by_filter(eventFilters: EventFiltersSchema, decoded_token: dict = Depends(verify_firebase_token)):
    try:
        filteredEventList = eventService.get_events_by_filter(eventFilters)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(jsonable_encoder(filteredEventList)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))
@eventsRouter.post("/create")
def create(event: EventSchema, decoded_token: dict = Depends(verify_firebase_token)):
    try:
        response = eventService.create_event(event)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=get_successful_response(response))
    except Exception as e:
        return JSONResponse(content= get_unsuccessful_response(e))