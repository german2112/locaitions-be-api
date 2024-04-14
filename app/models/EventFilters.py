from pydantic import BaseModel, Field
from app.models.Event import EventStatus

class EventFiltersSchema(BaseModel):

    class Config:
        arbitrary_types_allowed = True #Allow pydantic to validate arbitrary types

    uid: str = Field(None)
    name: str = Field(None)
    date: str = Field(None)
    clubId: str = Field(None)
    userId: str = Field(None)
    type: str = Field(None)
    location: object = Field(None)
    status: EventStatus = Field(None)