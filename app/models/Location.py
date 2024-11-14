from pydantic import BaseModel, Field, validator
from enum import Enum
from fastapi.encoders import jsonable_encoder
from typing import Optional

class Coordinates(BaseModel):
        class CoordinatesType(Enum):
            Point = "Point"
            Polygon = "Polygon"

        type: CoordinatesType
        coordinates: object

        def to_dict(self):
            coordinatesDict = self.dict()
            coordinatesDict["type"] = self.type.value
            coordinatesDict["coordinates"] = jsonable_encoder(self.coordinates)
            return coordinatesDict
    
    


class LocationSchema(BaseModel):

    class Config:
        arbitrary_types_allowed = True #Allow pydantic to validate arbitrary types
    
    mainCoordinates: Coordinates
    area: Optional[Coordinates] = Field(default_factory=None)
    name: str
    address: str

    def to_dict(self):
        locationDict = self.dict()
        locationDict["area"] = None if self.area == None else self.area.to_dict()
        locationDict["mainCoordinates"] = self.mainCoordinates.to_dict()
        return locationDict
