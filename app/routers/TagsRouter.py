from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.services import TagService as tagService
from app.utils.ResponseUtils import *
from fastapi.encoders import jsonable_encoder


tagsRouter = APIRouter(prefix="/tags")


@tagsRouter.get("/{search}", tags=["Tags"], description="Endpoint used for the tags auto complete")
def autocomplete_search(search: str):
    try:
        tags_found = tagService.autocomplete_search(search)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_successful_response(jsonable_encoder(tags_found)))
    except Exception as e:
        return JSONResponse(content=get_unsuccessful_response(e))
