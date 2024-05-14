from pydantic import BaseModel, Field, validator
from app.models.Location import LocationSchema
from app.models.Photo import PhotoSchema
from enum import Enum
from app.validators import DateValidators
from typing import List
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import Optional


class EventStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SCHEDULED = "SCHEDULED"


class EventSchema(BaseModel):

    class Config:
        arbitrary_types_allowed = True #Allow pydantic to validate arbitrary types
    _id: str = Field(default=None)
    name: str
    location: LocationSchema
    rating: float = Field(le=5, ge=0)
    createdDate: Optional[datetime] #TODO CHANGE TO DATETIME
    status: EventStatus
    type: str
    description: Optional[str]
    userId: str = Field(default= "")
    clubId: str = Field(default= "")
    startDate: str
    endDate: str
    photos: List[PhotoSchema] = Field(default_factory=list)
    tags: List[str] = Field(default=[])
    capacity: int
    
    @validator('startDate', 'endDate')
    def validate_dates(cls, value):
       return DateValidators.validate_date_in_YYYYMMDDHHmmFormat(value)
    
    def to_dict(self):
        eventDict = self.dict()
        eventDict["location"] = jsonable_encoder(self.location)
        eventDict["createdDate"] = str(self.createdDate)
        eventDict["status"] = self.status.value
        eventDict["photos"] = jsonable_encoder(self.photos)
        return eventDict