from fastapi import APIRouter, status
from app.models.User import UserSchema
from app.models.Event import EventSchema
from app.services import LiveVideoService
from app.dto.CreateLiveStreamDTO import CreateLiveStreamDTO
from app.utils.ResponseUtils import *
from fastapi.responses import JSONResponse

liveVideoRouter = APIRouter(prefix="/live-video")

@liveVideoRouter.post("/validate-user-location", response_description="Validate if user in specific location")
async def validate_user_location(user: UserSchema, event: EventSchema):
    response = LiveVideoService.validate_if_user_in_area(user, event)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@liveVideoRouter.get("/event-owner-streaming")
async def get_event_owner_stream(eventId: str, eventCreatedBy: str):
    try:
        resopnse = LiveVideoService.get_event_owner_stream(eventId, eventCreatedBy)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(resopnse))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))
    
@liveVideoRouter.post("/create-live-stream-video")
async def create(liveStreamData: CreateLiveStreamDTO):
    try:
        response = LiveVideoService.create_live_stream(liveStreamData)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=get_successful_response(response))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))