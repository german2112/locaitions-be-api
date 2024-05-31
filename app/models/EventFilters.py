from pydantic import BaseModel, Field
from app.models.Event import EventStatus
from app.models.Location import LocationSchema
from typing import List, Optional

class EventFiltersSchema(BaseModel):

    class Config:
        arbitrary_types_allowed = True #Allow pydantic to validate arbitrary types

    uid: str = Field(default = None)
    name: str = Field(default = None)
    startDate: str = Field(default = None)
    clubId: str = Field(default = None)
    userId: str = Field(default = None)
    type: str = Field(default = None)
    location: LocationSchema = Field(default = None)
    status: EventStatus = Field(default = None)
    tags: List[str] = Field(default=[])