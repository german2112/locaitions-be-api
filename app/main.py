# main.py
from fastapi import FastAPI
from config import database

app = FastAPI()



@app.get("/")
async def root():
 return database.db["Users"].find()