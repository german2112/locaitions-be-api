from pydantic import BaseModel, Field
from enum import Enum
from fastapi.encoders import jsonable_encoder

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
    area: Coordinates = Field(default_factory=dict)
    name: str
    address: str

    def to_dict(self):
        locationDict = self.dict()
        locationDict["area"] = jsonable_encoder(self.area) if self.area else {}
        locationDict["mainCoordinates"] = jsonable_encoder(self.mainCoordinates)
        return locationDict
