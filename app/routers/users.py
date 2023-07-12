from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.User import UserSchema
from config import database
from fastapi import APIRouter, Body, status

router = APIRouter

def find_user_by_phone(phone: int):
 user_exists = database.db["Users"].find_one({"phone": phone})
 return user_exists

def find_user_by_email(email: str):
 user_exists = database.db["Users"].find_one({"email": email})
 return user_exists

@router.post("/create-user", response_description="Create new user", response_model=UserSchema, tags=["users"])
def create_membership(user: UserSchema = Body(...)):
    if find_user_by_email(user.email) or find_user_by_phone(user.phone): 
      return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "User already exists"})
    user = jsonable_encoder(user)
    database.db["Users"].insert_one(user)  
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created"})