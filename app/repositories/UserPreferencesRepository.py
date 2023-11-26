from app.config import database

from app.models.UserPreferences import UserPreferencesSchema

def insert_music_genre_preferences(musicGenrePreferences: UserPreferencesSchema):
    return database.db["UserPreferences"].update_one({"userUid": musicGenrePreferences["userUid"]}, {"$set": musicGenrePreferences},upsert=True)
