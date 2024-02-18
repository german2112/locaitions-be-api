from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, status
from app.models.User import UserSchema
from app.services import UserService as userService
from app.utils import TypeUtilities as typeUtilities
from app.models.Photo import PhotoSchema
from app.models.User import SocialMedia
from app.models.UserPreferences import UserPreferencesSchema
from app.models.UserPreferences import UserPreferenceResponse
from typing import Annotated
from fastapi import UploadFile, Form
from typing import List

userRouter = APIRouter(prefix="/user")

@userRouter.post("/create", response_description="Create new user", response_model=UserSchema, tags=["Users"])
def create(user: UserSchema = Body(...)):
    response = typeUtilities.parse_json(userService.create_user(user))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

@userRouter.put("/update", response_description="Update user", response_model=UserSchema, tags=["Users"])
def update(user: UserSchema) :
  response = typeUtilities.parse_json(userService.update_user(user))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.get("/validate-username/{userName}", response_description="Validate username", response_model=bool, tags=["Users"])
def validate_username(userName: str):
  response = typeUtilities.parse_json(userService.validate_if_user_name_exist(userName))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.get("/profile/{uid}", response_description="public Profile user information", response_model=UserSchema, tags=["User", "Public", "Profile"])
def get_public_profile(uid: str):
  response = typeUtilities.parse_json(userService.get_public_profile(uid))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.get("/user-preferences/{uid}", response_description="Get list of music genres for user", response_model=UserPreferenceResponse, tags=["MusicGenre"])
def find_by_user(uid: str):
  response = typeUtilities.parse_json(userService.get_music_genre_preferences_by_user(uid))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.post("/upload-photo", response_description="Upload user photo", response_model=PhotoSchema, tags=["Users"])
async def upload_photo(files: Annotated[List[UploadFile], Form()], userUid: Annotated[str, Form()], isProfile: Annotated[bool, Form()]) :
  response = await userService.upload_photos(userUid,files, isProfile)
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.post("/musicgenre-preferences", response_description="Insert user's music genre preferences", response_model=bool, tags=["Users"])
def insert_music_genre_preferences(musicGenrePreferences: UserPreferencesSchema):
  response = typeUtilities.parse_json(userService.insert_music_genre_preferences(musicGenrePreferences))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.post("/social-media-link/{uid}", response_description="Update a social media link", response_model=SocialMedia, tags=["Users", "social_media_link"])
def update_social_media_link(uid: str, socialMediaItem: SocialMedia = Body(...)):
  response = typeUtilities.parse_json(userService.update_social_media_link(uid, socialMediaItem))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.delete("/social-media-link/{uid}", response_description="delete social media link", response_model=SocialMedia, tags=["Users", "social_media_link"])
def delete_social_media_link(uid: str, socialMediaItem: SocialMedia = Body(...)):
  response = typeUtilities.parse_json(userService.delete_social_media_link(uid, socialMediaItem))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)