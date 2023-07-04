from pydantic import BaseModel, Field
from typing import List
import Exclusivity
from .Promotion import PromotionSchema
from .Event import EventSchema

class ClubSchema(BaseModel):
    name: str = Field(..., max_length=40)
    location: str = Field(..., max_length=100)
    exclusivity: Exclusivity = Field(None)
    promotions: List[PromotionSchema] = Field(None)
    event: List[EventSchema] = Field(None)
