from app.repositories import UserRepository as userRepository
from app.models.User import UserSchema
from fastapi.encoders import jsonable_encoder

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