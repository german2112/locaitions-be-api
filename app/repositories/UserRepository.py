from app.config import database
from app.models.User import SocialMedia
from typing import List

def find_by_phone(phone: str):
    return database.db["Users"].find_one({"phone": phone})

def find_by_email(email: str):
    return database.db["Users"].find_one({"email": email})

def find_by_id(uid: str):
    return database.db["Users"].find_one({"uid": uid})

def find_by_userName(userName: str):
    return database.db["Users"].find_one({'userName': userName})

def insert_user(user):
    return database.db["Users"].insert_one(user)

def update_user(uid, user):
    return database.db["Users"].update_one({'uid': uid}, {'$set': user})

def update_user_photos(userUid: str, photos: List[dict]):
    filterCriteria = {'uid':userUid}
    updateCriteria = {'$push': {'photos': {'$each': photos}}}
    return database.db['Users'].update_one(filter=filterCriteria, update=updateCriteria)

def update_profile_picture(userUid: str, photo: dict):
    filterCriteria = {'uid':userUid}
    updateCriteria = {'$set': {'profilePicture': photo}}
    return database.db['Users'].update_one(filter=filterCriteria, update=updateCriteria)

def remove_social_media_link(uid: str, socialMediaItem: SocialMedia):
    socialMediaItem = {
    "url": socialMediaItem.url,
    "url_type": socialMediaItem.url_type.value
    }
    return database.db["Users"].update_one(
        {'uid': uid}, 
        {
            '$pull': { 
                'socialMediaLinks': { 'url_type': socialMediaItem['url_type'] }
            }
        }
    )

def delete_user_photo_by_id(uid: str, photoId: str):
    return database.db["Users"].update_one(
        {"uid": uid},
        {
            '$pull': {
                'photos': {'id': photoId}
            }
        }
    )