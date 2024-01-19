from pydantic import BaseModel, Field
from typing import List
from app.models.MusicGenre import MusicGenreSchema


class UserPreferencesSchema(BaseModel):
    userUid: str = Field(...)
    musicGenres: List[str] = Field(...)
    
class UserPreferenceResponse(BaseModel):
    userUid: str
    musicGenres: List[MusicGenreSchema]