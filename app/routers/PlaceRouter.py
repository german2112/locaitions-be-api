from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.models.Place import PlaceSchema
from app.models.User import UserSchema
from app.services import PlaceService as placeService
from app.utils import TypeUtilities as TypeUtilities

placeRouter = APIRouter(prefix="/place")

#Get All Places
@placeRouter.post("", response_description="Get list of places", response_model=PlaceSchema)
def find_all(user: UserSchema, place: PlaceSchema):
    response = TypeUtilities.parse_json(placeService.get_list_of_places(user, place))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


