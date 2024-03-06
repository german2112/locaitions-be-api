from app.config import database

from app.models.UserPreferences import UserPreferencesSchema
from app.entities.Filter import UserFilter

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
                "musicGenres": 1,
                "filters": 1
            }
        }
    ])

def insert_filter_preference(uid: str, new_filter: UserFilter):
    collection = database.db['UserPreferences']
    
    userPreferences: UserPreferencesSchema = collection.find_one({"userUid": uid})

    result = collection.update_one({
        "userUid": uid,
        "filters.name": new_filter["name"]
    }, {
        "$set": {"filters.$.value": new_filter["value"]}
    })
    
    if result.matched_count == 0:
        collection.update_one({"userUid": uid}, { "$push": {"filters": { "value": new_filter['value'], "name": new_filter['name'] }} })

    userPreferences = database.db['UserPreferences'].find_one({"userUid": uid})
    return userPreferences