from app.repositories import UserRepository as userRepository
from app.repositories import PhotoRepository as photoRepository
from app.models.User import UserSchema
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile
from datetime import datetime
from dotenv import load_dotenv
import boto3
import os

load_dotenv()

session = boto3.Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                        region_name=os.getenv("AWS_REGION")
                      )

def create_user(user: UserSchema):
  user_existing = validate_if_user_exist(user)
  if user_existing:
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
  update_user["userName"] = user.userName or update_user.get("userName", None)
  userRepository.update_user(user.uid,update_user)
  return {"message:": "OK","body" : update_user}

def validate_if_user_exist(user: UserSchema):
  userFound = {}
  userSearchList = [find_user_by_email(user.email), find_user_by_phone(user.phone), find_user_by_id(user.uid)]
  for user in userSearchList:
    if user != {}:
      userFound = user
      return userFound
  return userFound

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
async def upload_photo(userUid: str ,file: UploadFile):
  #TODO Insert name of the bucket into a constant file and import
  bucketName = "locaitions-api-staging"

  uploadedImageURL = ""

  if not is_image_explicit(file.file.read()):
    #Return pointer to the beggining of the file
    await file.seek(0)

    client = session.resource("s3")
    bucket = client.Bucket(bucketName)
    #TODO Verify ACLs configuration for prod env
    bucket.upload_fileobj(file.file, file.filename)
    uploadedImageURL = f"https://{bucketName}.s3.amazonaws.com/{file.filename}"

    uploadPhotoToDB = {
                      "filename": file.filename,
                       "fileUrl": uploadedImageURL,
                       "userUid": userUid,
                       "createdAt": datetime.now()
                       }
    photoRepository.upload_photo(jsonable_encoder(uploadPhotoToDB))

  return {"message:": "OK","body":uploadedImageURL}

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