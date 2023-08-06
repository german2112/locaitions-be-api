from app.repositories import UserRepository as userRepository
from app.models.User import UserSchema
from fastapi.encoders import jsonable_encoder

def create_user(user: UserSchema):
  user_existing = validate_if_user_exists(user)
  if user_existing:
      return user_existing
  user = jsonable_encoder(user)
  created_user_id = userRepository.insert_user(user).inserted_id
  created_user = find_user_by_id(created_user_id)
  return created_user

def update_user(user:UserSchema):
  if(user == None):
    return {}
  updated_user_id = userRepository.update_user(user.uid,jsonable_encoder(user))
  updated_user = find_user_by_id('64c6ad80f68acb3146b40ea3')
  return updated_user

def validate_if_user_exists(user: UserSchema):
  user = [find_user_by_email(user.email), find_user_by_phone(user.phone), find_user_by_id(user.uid)]
  for existingUser in user:
    if existingUser != None:
      return existingUser
  return {}

def find_user_by_phone(phone: str):
 return userRepository.find_by_phone(phone)

def find_user_by_email(email: str):
 return userRepository.find_by_email(email)

def find_user_by_id(uid: str):
  return userRepository.find_by_id(uid)