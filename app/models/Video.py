from pydantic import BaseModel, Field
from datetime import datetime

class VideoSchema(BaseModel):
    createdAt: datetime = Field(...)
    url: str = Field(...)
