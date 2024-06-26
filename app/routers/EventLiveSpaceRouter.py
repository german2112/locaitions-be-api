from fastapi import APIRouter, status
from app.services import EventLiveSpaceService
from app.dto.CreateLiveSpaceDTO import CreateLiveSpaceDTO
from app.utils.ResponseUtils import *
from fastapi.responses import JSONResponse

eventLiveSpaceRouter = APIRouter(prefix="/event-live-space")

@eventLiveSpaceRouter.post("/create-event-live-space")
async def create(liveStreamData: CreateLiveSpaceDTO):
    try:
        response = await EventLiveSpaceService.create_live_space(liveStreamData)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=get_successful_response(response))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))