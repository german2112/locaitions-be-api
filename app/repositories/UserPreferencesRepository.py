from app.config import database

from app.models.UserPreferences import UserPreferencesSchema

def insert_music_genre_preferences(musicGenrePreferences: UserPreferencesSchema):
    return database.db["UserPreferences"].update_one({"userUid": musicGenrePreferences["userUid"]}, {"$set": musicGenrePreferences},upsert=True)

def find_by_user_uid(uid: str):
    return database.db["UserPreferences"].aggregate([
        {
            "$match": {
                "userUid": uid
            }
        },
        {
            "$addFields": {
                "musicGenresIds": {
                    "$map": {
                        "input": "$musicGenres",
                        "as": "musicGenreId",
                        "in": {
                            "$toObjectId": "$$musicGenreId"
                        }
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "MusicGenres",
                "localField": "musicGenresIds",
                "foreignField": "_id",
                "as": "musicGenres",
            }
        },
        {
            "$project": {
                "_id": 1,
                "userUid": 1,
                "musicGenres": 1
            }
        }
    ])