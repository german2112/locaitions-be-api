from pydantic import BaseModel, Field
from datetime import datetime

class MusicGenreSchema(BaseModel):
    name: str = Field(..., max_length=40)
    #TODO createdAt: datetime = Field(...)