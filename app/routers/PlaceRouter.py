from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.models.Place import PlaceSchema
from app.models.User import UserSchema
from app.services import PlaceService as placeService
from app.utils import TypeUtilities as TypeUtilities
from fastapi_pagination import Params, paginate

placeRouter = APIRouter(prefix="/place")

#Get All Places
@placeRouter.post("", 
                  response_description="Get list of places"
                  )
def find_all(user: UserSchema, place: PlaceSchema, params: Params):
    response = TypeUtilities.parse_json(placeService.get_list_of_places(user, place))
    return paginate(response, params)


@placeRouter.get("/{placeId}", response_description="Get place by Id", response_model=PlaceSchema)
def get_by_id(placeId: str):
    response = TypeUtilities.parse_json(placeService.get_place_by_id(placeId))
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)