from app.repositories import UserRepository as userRepository
from app.repositories import PhotoRepository as photoRepository
from app.repositories import UserPreferencesRepository as userPreferencesRepository
from app.models.User import UserSchema
from app.models.UserPreferences import UserPreferencesSchema
from app.models.User import SocialMedia
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile
from datetime import datetime
from dotenv import load_dotenv
import boto3
import os
from copy import deepcopy

load_dotenv()

session = boto3.Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                        region_name=os.getenv("AWS_REGION")
                      )

def create_user(user: UserSchema):
  user_existing = validate_if_user_exist(user)
  if user_existing != None:
      return user_existing
  user = jsonable_encoder(user)
  userRepository.insert_user(user)
  created_user = find_user_by_id(user["uid"])
  return created_user

def update_user(user:UserSchema):
  update_user = userRepository.find_by_id(user.uid)
  if(update_user == None):
    return {"message:": "no user found with the given id","body" : {}}
  update_user["name"] = user.name or update_user.get("name", None)
  update_user["email"] = user.email or update_user.get("email", None)
  update_user["membership"] = user.membership or update_user.get("membership", None)
  update_user["phone"] = user.phone or update_user.get("phone", None)
  update_user["role"] = user.role or update_user.get("role", None)
  update_user["preferredClubs"] = user.preferredClubs or update_user.get("preferredClubs", None)
  update_user["location"] = user.location or update_user.get("location", None)
  update_user["mapsPlaceId"] = user.mapsPlaceId or update_user.get("mapsPlaceId", None)
  update_user["birthDate"] = user.birthDate or update_user.get("birthDate", None)
  update_user["userName"] = user.userName or update_user.get("userName", None)
  update_user["birthDate"] = user.birthDate or update_user.get("birthDate", None)
  update_user["nationality"] = user.nationality or update_user.get("nationality", None)
  try:
      update_user['gender'] = getattr(user.gender, 'value', None) or update_user.get("gender", None)
  except AttributeError:
      update_user['gender'] = update_user.get("gender", None)
  
  userRepository.update_user(user.uid,update_user)

  #TODO Response structure must be defined in the repository
  return {"message:": "OK","body" : update_user}

def validate_if_user_exist(user: UserSchema):
  foundUser = find_user_by_id(user.uid)
  if foundUser == None:
    return None
  return foundUser

def validate_if_user_name_exist(userName: str):
  userFound = {}
  if userName != None:
    userFound = userRepository.find_by_userName(userName)
  return userFound != None

def find_user_by_phone(phone: str):
 foundUser = {}
 if phone != None :
   foundUser = userRepository.find_by_phone(phone)
 return foundUser

def find_user_by_email(email: str):
 foundUser = {}
 if email != None :
   foundUser = userRepository.find_by_email(email)
 return foundUser

def find_user_by_id(uid: str):
  foundUser = {}
  if uid != None :
   foundUser = userRepository.find_by_id(uid)
  return foundUser

#TODO Simplify the method in sub-methods
async def upload_photos(userUid: str ,files: List[UploadFile]):
  #TODO Insert name of the bucket into a constant file and import
  bucketName = "locaitions-api-staging"

  uploadedImageURL = ""
  
  uploadedImageUrls: List[str] = []
  
  for file in files:
    if not is_image_explicit(file.file.read()):
      #Return pointer to the beggining of the file
      #TODO Verify ACLs configuration for prod env
      await file.seek(0)
      client = session.resource("s3")
      bucket = client.Bucket(bucketName)
      bucket.upload_fileobj(file.file, file.filename)
      uploadedImageURL = f"https://{bucketName}.s3.amazonaws.com/{file.filename}"
      uploadedImageUrls.append(uploadedImageURL)
      uploadPhotoToDB = {
                      "filename": file.filename,
                       "fileUrl": uploadedImageURL,
                       "userUid": userUid,
                       "createdAt": datetime.now()
                      }
      photoRepository.upload_photo(jsonable_encoder(uploadPhotoToDB))

  return {"message:": "OK","body":uploadedImageUrls}

def is_image_explicit(content: bytes):
  client = session.client('rekognition')
  
  response = client.detect_moderation_labels(Image={'Bytes': content})

  #TODO Migrate to enum class
  explictyDefinition = {"Explicit Nudity":"Explicit Nudity",
                         "Suggestive":"Suggestive",
                         "Violence":"Violence",
                         "Visual Disturbing":"Visual Disturbing",
                         "Rude Gestures":"Rude Gestures",
                         "Drugs":"Drugs",
                         "Tobacco":"Tobacco",
                         "Alcohol":"Alcohol",
                         "Gambling":"Gambling",
                         "Hate Symbols":"Symbols"}

  for label in response['ModerationLabels']:
      if explictyDefinition.get(label.get("ParentName")):
        return True
      
  return False

def insert_music_genre_preferences(musicGenrePreferences: UserPreferencesSchema):
  try:
    userPreferencesRepository.insert_music_genre_preferences(jsonable_encoder(musicGenrePreferences))
    return {"message": "Request processed successfully"}
  except:
    return {"message": "Request Failed to add music genres"}
  #TODO modify response message for failure scenario, raise exception in case of failure

def get_music_genre_preferences_by_user(uid: str):
  try:
    user_preferences = userPreferencesRepository.find_by_user_uid(uid)
    preferences = list(user_preferences)
    for preference in preferences:
     preference["_id"] = str(preference["_id"])
     for musicGenre in preference['musicGenres']:
       musicGenre["_id"] = str(musicGenre["_id"])
    return {"body": preferences[0] if preferences and len(preferences) > 0 else preferences}
  except:
    return {"message": "error while fetching user music genre preferences"}


def update_social_media_link(uid: str, socialMediaItem: SocialMedia):
  update_user: UserSchema = find_user_by_id(uid)
  
  if(update_user == None):
    return {"message": "No user found with that uid"}
  
  user_item = deepcopy(update_user)
  
  social_media_links: List[SocialMedia] = []
  
  if 'socialMediaLinks' in dir(user_item) or user_item['socialMediaLinks'] != None:
    social_media_links = user_item['socialMediaLinks']
  else:
    user_item['socialMediaLinks'] = [{'url_type': socialMediaItem.url_type.value, 'url': socialMediaItem.url}]
  
  found_social_media_index: int = None
  
  for i, social_media in enumerate(social_media_links):
    if(social_media['url_type'] == socialMediaItem.url_type.value):
      found_social_media_index = i
      break
  
  if found_social_media_index != None:
    social_media_links[found_social_media_index] = {
      'url': socialMediaItem.url,
      'url_type': socialMediaItem.url_type.value
    }
    user_item['socialMediaLinks'] = social_media_links
  else:
    socialMediaItem = vars(socialMediaItem)
    socialMediaItem['url_type'] = socialMediaItem['url_type'].value
    social_media_links.append(socialMediaItem)
    user_item['socialMediaLinks'] = social_media_links
  
  userRepository.update_user(uid, user_item)
  
  return {"message": "OK","body" : user_item['socialMediaLinks']}

def delete_social_media_link(uid: str ,socialMediaItem: SocialMedia):
  userRepository.remove_social_media_link(uid, socialMediaItem)
  user: UserSchema = find_user_by_id(uid)
  social_media_links: List[SocialMedia] = user.get('socialMediaLinks')
  return {"message": "OK", "body": social_media_links}