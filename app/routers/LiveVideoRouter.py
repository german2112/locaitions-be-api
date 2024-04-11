from fastapi import APIRouter, status
from app.models.User import UserSchema
from app.models.Event import EventSchema
from app.services import LiveVideoService
from fastapi.responses import JSONResponse

liveVideoRouter = APIRouter(prefix="/live-video")

@liveVideoRouter.post("/validate-user-location", response_description="Validate if user in specific location")
async def validate_user_location(user: UserSchema, event: EventSchema):
    response = LiveVideoService.validate_if_user_in_area(user, event)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
