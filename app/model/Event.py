from pydantic import BaseModel, Field
from typing import List
import datetime
import Video
from .Comment import CommentSchema

class EventSchema(BaseModel):
    name: str = Field(..., max_length=40)
    rating: int = Field(..., le=5, ge=0)
    date: datetime = Field(...)
    video: Video = Field(None)
    comment: List[CommentSchema] = Field(None)