from pydantic import BaseModel, Field, EmailStr
from typing import List
from .Membership import MembershipSchema
from .Role import RoleSchema
from .Place import PlaceSchema
from app.models.Photo import PhotoSchema
from enum import Enum
from app.models.UserPreferences import UserPreferencesSchema

class SocialMediaTypes(Enum):
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    YOUTUBE = "Youtube"
    TIKTOK = "TikTok"
    
class SocialMedia(BaseModel):
    url_type: SocialMediaTypes
    url: str
    
class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

class UserSchema(BaseModel):
    name: str = Field(None, max_length=40)
    email: EmailStr = Field(None)
    mapsPlaceId: str = Field(None)
    location: object = Field(None)
    birthDate: str = Field(None)
    membership: MembershipSchema = Field(None)
    phone: str = Field(None)
    role: RoleSchema = Field(None)
    preferredClubs: List[PlaceSchema] = Field(None)
    uid: str = Field(None)
    userName: str = Field(None, max_length=15)
    socialMediaLinks: List[SocialMedia] = Field(None)
    gender: Gender = Field(None)
    nationality: str = Field(None)
    preferences: UserPreferencesSchema = Field(None)
    agoraChatUser: str = Field(None)
    agoraLiveVideoUser: int= Field(None) #TODO Change to required
    photos: List[PhotoSchema] = Field(default_factory=list)
    
    def to_dict(self):
        exclude_keys = ['__special__', 'function_variable']

        # Create a new dictionary with only desired fields
        # This is also added so that we can use this object as a dict without the serialized functions
        filtered_data = {key: getattr(self, key) for key in dir(self) if key not in exclude_keys and not callable(getattr(self, key))}

        return filtered_data
    