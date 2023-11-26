from pydantic import BaseModel, Field
from typing import List
from .Exclusivity import ExclusivitySchema
from .Promotion import PromotionSchema
from .Event import EventSchema
class PlaceSchema(BaseModel):
    uid: str = Field(None)
    name: str = Field(None, max_length=40)
    address: str = Field(None, max_length=100)
    category: str = Field(None, max_length=30)
    minimumDistance: float = Field(None)
    exclusivity: ExclusivitySchema = Field(None)
    promotions: List[PromotionSchema] = Field(None)
    event: List[EventSchema] = Field(None)
