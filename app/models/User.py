from pydantic import BaseModel, Field, EmailStr
from typing import List
from .Membership import MembershipSchema
from .Role import RoleSchema
from .Place import PlaceSchema


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
    uid: str = Field(...)
    userName: str = Field(None, max_length=15)