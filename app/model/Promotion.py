from pydantic import BaseModel, Field

class PromotionSchema(BaseModel):
    name: str = Field(..., max_length=40)
    description: str = Field(..., max_length=255)