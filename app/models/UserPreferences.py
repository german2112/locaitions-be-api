from pydantic import BaseModel, Field
from typing import List


class UserPreferencesSchema(BaseModel):
    userUid: str = Field(...)
    musicGenres: List[str] = Field(...)