from pydantic import BaseModel, Field, validator
from app.models.Location import LocationSchema
from enum import Enum
from app.validators import DateValidators

class EventStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SCHEDULED = "SCHEDULED"


class EventSchema(BaseModel):

    class Config:
        arbitrary_types_allowed = True #Allow pydantic to validate arbitrary types

    name: str
    location: LocationSchema
    rating: float = Field(le=5, ge=0)
    date: str #TODO CHANGE TO DATETIME
    status: EventStatus
    type: str
    description: str
    userId: str = Field(default= "")
    clubId: str = Field(default= "")
    startDate: str
    endDate: str
    
    @validator('startDate', 'endDate')
    def validate_dates(cls, value):
       return DateValidators.validate_date_in_YYYYMMDDHHmmFormat(value)