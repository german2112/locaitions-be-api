from fastapi import FastAPI, Body, status
from config import database
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from model.Membership import MembershipSchema 

app = FastAPI()

@app.get("/")
async def root():
 return database.db["User"].find()

@app.post("/addMembership", response_description="Add new memership", response_model=MembershipSchema)
async def create_membership(membership: MembershipSchema = Body(...)):
    membership = jsonable_encoder(membership)
    new_membership = database.db["Memberships"].insert_one(membership)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=True)