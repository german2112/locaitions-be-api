from pydantic import BaseModel, Field
from app.models.Location import LocationSchema
from app.models.Photo import PhotoSchema
from typing import List

class PlaceSchema(BaseModel):
    id: str
    name: str
    category: str
    location: LocationSchema
    avgRating: float = Field(le=5, ge=0, default=0.0)
    ownerId: str
    description: str
    photos: List[PhotoSchema] = Field(default_factory=list)

    def to_dict(self):
        placeDict = self.dict()
        placeDict["location"] = self.location.to_dict()
        return placeDict