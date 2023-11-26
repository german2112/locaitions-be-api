from fastapi.responses import JSONResponse
from fastapi import APIRouter, status
from app.services import MusicGenreService as musicGenreService
from app.models.MusicGenre import MusicGenreSchema
from app.utils import TypeUtilities as typeUtilities

userRouter = APIRouter(prefix="/music-genre")

@userRouter.get("", response_description="Get list of music genres", response_model=MusicGenreSchema, tags=["MusicGenre"])
def find_all():
  response = typeUtilities.parse_json(musicGenreService.get_music_genre_list())
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.post("/create", response_description="Add music genre", response_model=MusicGenreSchema, tags=["MusicGenre"])
def create(musicGenre: MusicGenreSchema):
  response = typeUtilities.parse_json(musicGenreService.insert_music_genre(musicGenre))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)