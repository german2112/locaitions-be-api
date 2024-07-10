from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from app.schemas.EventFilter import EventFilter
from app.models.Event import EventSchema
from app.services import EventService as eventService
from app.schemas.CreateEvent import CreateEvent
from app.common.token_verification import verify_firebase_token
from typing import Annotated, List
from app.utils.ResponseUtils import *
from fastapi import UploadFile, Form
from fastapi_pagination import Params, paginate
from app.utils import TypeUtilities as TypeUtilities

eventRouter = APIRouter(prefix="/events")


@eventRouter.post("/filter-event", tags=["Events"], description="Filtering the events")
def find_by_filter(eventFilters: EventFilter, params: Params, decoded_token: dict = Depends(verify_firebase_token)):
    try:
        response = TypeUtilities.parse_json(eventService.get_events_by_filter(eventFilters))
        return paginate(response, params)
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))

@eventRouter.post("/create", tags=["Events"], description="Create the event")
def create(event: CreateEvent, decoded_token: dict = Depends(verify_firebase_token)):
    try:
        response = eventService.create_event(event)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=get_successful_response(response))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))


@eventRouter.post("/upload-photo", tags=["Events"], description="Upload a photo related to an event")
async def upload_photo(files: Annotated[List[UploadFile], Form()], eventId: Annotated[str, Form()], isProfile: Annotated[bool, Form()] = False, decoded_token: dict = Depends(verify_firebase_token)):
    try:
        response = await eventService.upload_event_photos(eventId, files, isProfile)
        return JSONResponse(status_code=200, content=get_successful_response(TypeUtilities.parse_json(response)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))


@eventRouter.get("/{event_id}", tags=["Events"], description="Get a specific event by id")
def find_by_id(event_id: str, decoded_token: dict = Depends(verify_firebase_token)):
    try:
        response = eventService.find_by_id(event_id=event_id)
        return JSONResponse(status_code=200, content=get_successful_response(TypeUtilities.parse_json(response)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))
