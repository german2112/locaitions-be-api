from app.config import database

def upload_photo(photo):
    return database.db["Photos"].insert_one(photo)