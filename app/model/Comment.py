from pydantic import BaseModel, Field
import datetime

class CommentSchema(BaseModel):
    description: str = Field(..., max_length=255)
    createdAt: datetime = Field(...)