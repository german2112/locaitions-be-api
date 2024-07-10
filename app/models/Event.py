from pydantic import BaseModel, Field, validator, Extra
from app.models.Location import LocationSchema
from app.models.Photo import PhotoSchema
from app.models.Tag import TagSchema
from enum import Enum
from app.validators import DateValidators
from typing import List, Optional
from datetime import datetime

class EventStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SCHEDULED = "SCHEDULED"


class EventSchema(BaseModel):

    class Config:
        arbitrary_types_allowed = True #Allow pydantic to validate arbitrary types
        extra = Extra.forbid
    id: str = Field(default=None)
    name: str
    location: LocationSchema
    rating: float = Field(le=5, ge=0)
    createdDate: datetime #TODO CHANGE TO DATETIME
    status: EventStatus
    type: str
    description: str = Field(default="")
    userId: str = Field(default= "")
    clubId: str = Field(default= "")
    startDate: str
    endDate: str
    tags: List[TagSchema] = Field(default_factory=[])
    photos: List[PhotoSchema] = Field(default_factory=list)
    capacity: int
    isPrivate: bool
    chatroomId: str

    @validator('startDate', 'endDate')
    def validate_dates(cls, value):
        return DateValidators.validate_date_in_YYYYMMDDHHmmFormat(value)

    def to_dict(self):
        eventDict = self.dict()
        eventDict["location"] = self.location.to_dict()
        eventDict["createdDate"] = str(self.createdDate)
        eventDict["status"] = self.status.value
        return eventDict
