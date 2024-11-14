from pydantic import BaseModel, Field
from typing import List
from app.models.Tag import TagSchema
from app.models.Location import LocationSchema

class CreateEvent(BaseModel):
    name: str
    description: str
    status: str
    type: str
    capacity: int
    isPrivate: bool
    tags: List[TagSchema]
    clubId: str = Field(default='')
    userId: str = Field(default='')
    startDate: str
    endDate: str
    location: LocationSchema