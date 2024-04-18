from pydantic import BaseModel, Field
from enum import Enum

class Coordinates(BaseModel):
        class CoordinatesType(Enum):
            Point = "Point"
            Polygon = "Polygon"

        type: CoordinatesType
        coordinates: object

class LocationSchema(BaseModel):

    class Config:
        arbitrary_types_allowed = True #Allow pydantic to validate arbitrary types
    
    mainCoordinates: Coordinates
    area: Coordinates = Field(default = {})
    name: str
    address: str