from fastapi import FastAPI, Body, status
from config import database
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.User import UserSchema 

app = FastAPI()

@app.get("/")
async def root():
 database.db["Users"].find()
 return database.db["Users"].find()

def find_user_by_phone(phone: str):
 user_exists = database.db["Users"].find_one({"phone": phone})
 return user_exists

def find_user_by_email(email: str):
 user_exists = database.db["Users"].find_one({"email": email})
 return user_exists

def find_user_by_id(uid: str):
  user_exists = database.db["Users"].find_one({"uid": uid})
  return user_exists

@app.post("/initialize-user", response_description="Create new user", response_model=UserSchema, tags=["users"])
def create_membership(user: UserSchema = Body(...)):
    if find_user_by_email(user.email) or find_user_by_phone(user.phone) or find_user_by_id(user.uid): 
      return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "User already exists"})
    user = jsonable_encoder(user)
    created_user = database.db["Users"].insert_one(user)
    response: str = "user created with id"+created_user.inserted_id
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": response})