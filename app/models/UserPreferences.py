from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.MusicGenre import MusicGenreSchema
from app.entities.Filter import UserFilter


class UserPreferencesSchema(BaseModel):
    userUid: str = Field(...)
    musicGenres: List[str] = Field(...)
    filters: Optional[List[UserFilter]] = Field(default=[])
    class Config:
        arbitrary_types_allowed = True
    
class UserPreferenceResponse(BaseModel):
    userUid: str
    musicGenres: List[MusicGenreSchema]
    filters: List[UserFilter] = Field(...)
    class Config:
        arbitrary_types_allowed = True