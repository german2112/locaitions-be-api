from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.models.Club import ClubSchema
from app.models.User import UserSchema
from app.services import PlaceService as placeService
from app.utils import TypeUtilities as TypeUtilities

placeRouter = APIRouter(prefix="/place")

#Get All Places
@placeRouter.get("", response_description="Get list of places", response_model=ClubSchema)
def find_all(user: UserSchema):
    response = TypeUtilities.parse_json(placeService.get_list_of_places(user))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


