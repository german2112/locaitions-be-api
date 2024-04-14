from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .Video import VideoSchema
from .Comment import CommentSchema
from enum import Enum

class EventStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SCHEDULED = "SCHEDULED"

class EventSchema(BaseModel):
    uid: str = Field(None)
    name: str = Field(..., max_length=40)
    rating: int = Field(..., le=5, ge=0)
    date: datetime = Field(None)#TODO CHANGE TO REQUIRED
    video: VideoSchema = Field(None)
    comment: List[CommentSchema] = Field(None)
    status: EventStatus = Field(None)