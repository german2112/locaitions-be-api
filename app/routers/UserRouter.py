from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, status
from app.models.User import UserSchema
from app.config import database
from app.services import UserService as userService

userRouter = APIRouter(prefix="/user")

@userRouter.post("/create", response_description="Create new user", response_model=UserSchema, tags=["users"])
def create(user: UserSchema = Body(...)):
    if userService.find_user_by_email(user.email) or userService.find_user_by_phone(user.phone) or userService.find_user_by_id(user.uid): 
      return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "User already exists"})
    user = jsonable_encoder(user)
    created_user = database.db["Users"].insert_one(user)
    response: str = "user created with id"+created_user.inserted_id
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": response})

@userRouter.put("/update", response_description="Update user", response_model=UserSchema)
def update(user: UserSchema) :
  if(user == None):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User cannot be null"})
  updated_user = database.db["Users"].update_one({'uid': user.uid})

  return JSONResponse(status_code=status.HTTP_200_OK, content=updated_user)