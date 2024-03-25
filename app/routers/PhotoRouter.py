from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends
from app.models.Photo import PhotoSchema
from app.services import PhotoService as photoService
from app.common.token_verification import verify_firebase_token

from app.utils import TypeUtilities as TypeUtilities

from typing import List


userRouter = APIRouter(prefix="/photo")

@userRouter.get("/{uid}", response_description="pictures", response_model=List[PhotoSchema], tags=["Users", "Photos"])
def find_by_user_uid(uid: str, decoded_token: dict = Depends(verify_firebase_token)):
  response = TypeUtilities.parse_json(photoService.find_photos_by_user_uid(uid))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.delete("/{id}", response_description="pictures deleted", response_model=bool, tags=['Photos', 'Deletion'])
def delete_photo(id: str, decoded_token: dict = Depends(verify_firebase_token)):
  response = TypeUtilities.parse_json(photoService.find_photo_and_delete(id))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)