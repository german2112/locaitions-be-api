from pydantic import BaseModel, Field
from app.models.Location import LocationSchema

class PlaceFilter(BaseModel):
    id: str = Field(default="")
    name: str = Field(default="")
    category: str = Field(default="")
    location: LocationSchema = Field(default=None)
    minimumDistance: float = Field(default=0.0)
    avgRating: float = Field(le=5, ge=0, default=0.0)
    ownerId: str = Field(default="")
    description: str = Field(default="")