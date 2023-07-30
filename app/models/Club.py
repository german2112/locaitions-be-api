from pydantic import BaseModel, Field
from typing import List
from .Exclusivity import ExclusivitySchema
from .Promotion import PromotionSchema
from .Event import EventSchema
class ClubSchema(BaseModel):
    uid: str = Field(...)
    name: str = Field(..., max_length=40)
    location: str = Field(..., max_length=100)
    exclusivity: ExclusivitySchema = Field(None)
    promotions: List[PromotionSchema] = Field(None)
    event: List[EventSchema] = Field(None)
