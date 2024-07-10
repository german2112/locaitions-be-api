from app.repositories import UserRepository as userRepository
from app.repositories import PhotoRepository as photoRepository
from app.repositories import UserPreferencesRepository as userPreferencesRepository
from app.models.User import UserSchema
from app.models.UserPreferences import UserPreferencesSchema
from app.models.User import SocialMedia
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile
from datetime import datetime, UTC
import os
from copy import deepcopy
from app.entities.Filter import UserFilter
from app.helpers.AgoraHelper import generate_app_token
import httpx
import uuid
from app.utils.TypeUtilities import encode_string_to_integer
from app.exceptions.BadRequestException import BadRequestException
from app.helpers.PhotoHelper import format_photos_to_insert

async def create_user(user: UserSchema):
    userExisting = validate_if_user_exist(user)
    if userExisting != None:
        return userExisting
    user = jsonable_encoder(user)
    agoraUser = await _generate_agora_user(user["uid"])
    user["agoraChatUser"] = agoraUser["username"]
    user["agoraLiveVideoUser"] = encode_string_to_integer(user["uid"]) #Encode UID to integer and save it as string as mongo's limit are 8-byte integers
    user["profilePicture"] = None
    userRepository.insert_user(user)
    createdUser = get_user_by_id(user["uid"])
    return createdUser


async def _generate_agora_user(uid: str):
    appToken = generate_app_token()
    userData = {
        "username": f"user-x-{uid[-4:]}",
        "password": str(uuid.uuid4())
    }
    headers = {"Authorization": f"Bearer {appToken['body']}"}
    requestUrl = f'https://{os.getenv("AGORA_CHAT_HOST")}/{os.getenv("AGORA_ORG_NAME")}/{os.getenv("AGORA_APP_NAME")}/users'
    async with httpx.AsyncClient() as client:
        response = await client.post(requestUrl, headers=headers, json=userData)
        if response.status_code == 200:
            return userData
           
        
def update_user(user: UserSchema):
    updateUser = userRepository.find_by_id(user.uid)
    if (updateUser == None):
        return {"message:": "no user found with the given id", "body": {}}
    updateUser["name"] = user.name or updateUser.get("name", None)
    updateUser["email"] = user.email or updateUser.get("email", None)
    updateUser["membership"] = user.membership or updateUser.get(
        "membership", None)
    updateUser["phone"] = user.phone or updateUser.get("phone", None)
    updateUser["role"] = user.role or updateUser.get("role", None)
    updateUser["preferredClubs"] = user.preferredClubs or updateUser.get(
        "preferredClubs", None)
    updateUser["location"] = user.location or updateUser.get(
        "location", None)
    updateUser["mapsPlaceId"] = user.mapsPlaceId or updateUser.get(
        "mapsPlaceId", None)
    updateUser["birthDate"] = user.birthDate or updateUser.get(
        "birthDate", None)
    updateUser["userName"] = user.userName or updateUser.get(
        "userName", None)
    updateUser["birthDate"] = user.birthDate or updateUser.get(
        "birthDate", None)
    updateUser["nationality"] = user.nationality or updateUser.get(
        "nationality", None)
    updateUser["role"] = user.role.value or updateUser.get(
        "role", None)
    try:
        updateUser['gender'] = getattr(
            user.gender, 'value', None) or updateUser.get("gender", None)
    except AttributeError:
        updateUser['gender'] = updateUser.get("gender", None)

    userRepository.update_user(user.uid, updateUser)

    # TODO Response structure must be defined in the repository
    return {"message:": "OK", "body": updateUser}


def validate_if_user_exist(user: UserSchema):
    try:
        foundUser = get_user_by_id(user.uid)
        userPreferences = userPreferencesRepository.find_by_user_uid(user.uid)
    except Exception as e:
        return {"message": "Error while getting user preferences"}
    else:
        if foundUser == None:
            return None

        userPreferences = list(userPreferences)
        if len(userPreferences) > 0:
            foundUser["preferences"] = userPreferences[0]
    return foundUser


def validate_if_user_name_exist(userName: str):
    userFound = {}
    if userName != None:
        userFound = userRepository.find_by_userName(userName)
    return userFound != None


def find_user_by_phone(phone: str):
    foundUser = {}
    if phone != None:
        foundUser = userRepository.find_by_phone(phone)
    return foundUser


def find_user_by_email(email: str):
    foundUser = {}
    if email != None:
        foundUser = userRepository.find_by_email(email)
    return foundUser


def get_user_by_id(uid: str):
    foundUser = {}
    if uid != None:
        foundUser = userRepository.find_by_id(uid)
    return foundUser

# TODO Simplify the method in sub-methods


async def upload_user_photos(userUid: str, files: List[UploadFile], isProfile: bool):
    userToUpdate = userRepository.find_by_id(userUid)
    if not userToUpdate:
        raise BadRequestException("No user found with the given uid")
    formattedPhotosList = await format_photos_to_insert(files, isProfile)

    if not isProfile or isProfile is None:
        userRepository.update_user_photos(userUid, formattedPhotosList)
    else:
        userRepository.update_profile_picture(userUid, formattedPhotosList[0])

    return {"message:": "OK", "body": jsonable_encoder(formattedPhotosList)}

def insert_music_genre_preferences(musicGenrePreferences: UserPreferencesSchema):
    try:
        userPreferencesRepository.insert_music_genre_preferences(
            jsonable_encoder(musicGenrePreferences))
        return {"message": "Request processed successfully"}
    except:
        return {"message": "Request Failed to add music genres"}
    # TODO modify response message for failure scenario, raise exception in case of failure


def get_music_genre_preferences_by_user(uid: str):
    try:
        userPreferences = userPreferencesRepository.find_by_user_uid(uid)
        preferences = list(userPreferences)
        for preference in preferences:
            preference["_id"] = str(preference["_id"])
            for musicGenre in preference['musicGenres']:
                musicGenre["_id"] = str(musicGenre["_id"])
        return {"body": preferences[0] if preferences and len(preferences) > 0 else preferences}
    except:
        return {"message": "error while fetching user music genre preferences"}

def update_social_media_link(uid: str, socialMediaItem: SocialMedia):
    updateUser: UserSchema = get_user_by_id(uid)

    if (updateUser == None):
        return {"message": "No user found with that uid"}

    userItem = deepcopy(updateUser)

    socialMediaLinks: List[SocialMedia] = []

    if 'socialMediaLinks' in dir(userItem) or userItem['socialMediaLinks'] != None:
        socialMediaLinks = userItem['socialMediaLinks']
    else:
        userItem['socialMediaLinks'] = [
            {'url_type': socialMediaItem.url_type.value, 'url': socialMediaItem.url}]

    foundSocialMediaIndex: int = None

    for i, social_media in enumerate(socialMediaLinks):
        if (social_media['url_type'] == socialMediaItem.url_type.value):
            foundSocialMediaIndex = i
            break

    if foundSocialMediaIndex != None:
        socialMediaLinks[foundSocialMediaIndex] = {
            'url': socialMediaItem.url,
            'url_type': socialMediaItem.url_type.value
        }
        userItem['socialMediaLinks'] = socialMediaLinks
    else:
        socialMediaItem = vars(socialMediaItem)
        socialMediaItem['url_type'] = socialMediaItem['url_type'].value
        socialMediaLinks.append(socialMediaItem)
        userItem['socialMediaLinks'] = socialMediaLinks

    userRepository.update_user(uid, userItem)

    return {"message": "OK", "body": userItem['socialMediaLinks']}


def delete_social_media_link(uid: str, socialMediaItem: SocialMedia):
    userRepository.remove_social_media_link(uid, socialMediaItem)
    user: UserSchema = get_user_by_id(uid)
    socialMediaLinks: List[SocialMedia] = user.get('socialMediaLinks')
    return {"message": "OK", "body": socialMediaLinks}


def get_public_profile(uid: str):
    foundUser = userRepository.find_by_id(uid)
    foundUserPictures = list(photoRepository.find_by_user_uid(uid))
    formattedUser = {
        'name': foundUser.get('name', None),
        'email': foundUser.get('email', None),
        'location': foundUser.get('location', None),
        'birthDate': foundUser.get('birthDate', None),
        'phone': foundUser.get('phone', None),
        'uid': foundUser.get('uid', None),
        'userName': foundUser.get('userName', None),
        'socialMediaLinks': foundUser.get('socialMediaLinks', None),
        'gender': foundUser.get('gender', None),
        'nationality': foundUser.get('nationality', None),
        'userPictures': foundUserPictures
    }
    return {"message": "OK", "body": formattedUser}


def insert_filter_preference(uid: str, filter: UserFilter):
    updatedPeferences = userPreferencesRepository.insert_filter_preference(
        uid, filter)
    return {"message": "OK", "body": updatedPeferences}

def delete_user_photo(userUid: str, photoId: str):
    """ bucketName = constants.AWS_BUCKET_NAME
    client = session.resource("s3")
    bucket = client.Bucket(bucketName)
    
    bucket.delete_objects() """

    userRepository.delete_user_photo_by_id(userUid, photoId)
    return {"message": "ok"}
    