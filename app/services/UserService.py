from app.repositories import UserRepository as userRepository

def find_user_by_phone(phone: str):
 return userRepository.find_by_phone(phone)

def find_user_by_email(email: str):
 return userRepository.find_by_email(email)

def find_user_by_id(uid: str):
  return userRepository.find_by_id(uid)