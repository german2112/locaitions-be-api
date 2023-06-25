from pydantic import BaseModel, Field, EmailStr
from typing import List
import Membership
import Role
from .Club import ClubSchema


class UserSchema(BaseModel):
    name: str = Field(..., max_length=40)
    email: EmailStr = Field(..., max_length=30)
    location: str = Field(..., max_length=100)
    membership: Membership = Field(...)
    role: Role = Field(...)
    preferredClubs: List[ClubSchema] = Field(...)
    