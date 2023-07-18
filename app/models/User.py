from pydantic import BaseModel, Field, EmailStr
from typing import List
from .Membership import MembershipSchema
from .Role import RoleSchema
from .Club import ClubSchema


class UserSchema(BaseModel):
    name: str = Field(..., max_length=40)
    email: EmailStr = Field(...)
    location: str = Field(..., max_length=100)
    membership: MembershipSchema = Field(...)
    phone: int = Field(...)
    role: RoleSchema = Field(None)
    preferredClubs: List[ClubSchema] = Field(None)
    uid: str = Field(...)
    