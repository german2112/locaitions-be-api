from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from app.models.Place import PlaceSchema
from app.models.User import UserSchema
from app.schemas.PlaceFilter import PlaceFilter
from app.services import PlaceService as placeService
from app.utils import TypeUtilities as TypeUtilities
from app.utils.ResponseUtils import *
from fastapi_pagination import Params, paginate


placeRouter = APIRouter(prefix="/place")

#Get All Places
@placeRouter.post("", response_description="Get list of places")
def get_places_by_filters(user: UserSchema, placeFilters: PlaceFilter, params: Params):
    try:
        response = TypeUtilities.parse_json(placeService.filter_list_of_places(user, placeFilters))
        return paginate(response,params)
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))

@placeRouter.get("/get-by-id/{placeId}", response_description="Get place by Id", response_model=PlaceSchema)
def get_by_id(placeId: str):
    try:
        response = TypeUtilities.parse_json(placeService.get_place_by_id(placeId))
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(response))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))

@placeRouter.get("/get-place-event", tags=["Places"], description="Get the active event of a place in a specific location")
def get_place_event(placeId: str, longitude: float, lattitude: float, status: str):
    try:
        response = placeService.get_place_event(placeId, longitude, lattitude, status)
        return JSONResponse(status_code=200, content=get_successful_response(TypeUtilities.parse_json(response)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))