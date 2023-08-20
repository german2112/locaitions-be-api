from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, status
from app.models.User import UserSchema
from app.services import UserService as userService
from app.utils import TypeUtilities as typeUtilities

userRouter = APIRouter(prefix="/user")

@userRouter.post("/create", response_description="Create new user", response_model=UserSchema, tags=["users"])
def create(user: UserSchema = Body(...)):
    response = typeUtilities.parse_json(userService.create_user(user))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

@userRouter.put("/update", response_description="Update user", response_model=UserSchema)
def update(user: UserSchema) :
  response = typeUtilities.parse_json(userService.update_user(user))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)

@userRouter.get("/validateUserName", response_description="Validate username", response_model=bool)
def validateUserName(userName: str):
  response = typeUtilities.parse_json(userService.validate_if_user_name_exist(userName))
  return JSONResponse(status_code=status.HTTP_200_OK, content=response)