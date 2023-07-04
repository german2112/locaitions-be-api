from pydantic import BaseModel, Field
import datetime

class VideoSchema(BaseModel):
    createdAt: datetime = Field(...)
    url: str = Field(...)
