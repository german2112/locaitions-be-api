from pydantic import BaseModel, Field
from datetime import datetime
class PhotoSchema(BaseModel):
    filename: str = Field(..., max_length=40)
    fileUrl: str = Field(..., max_length=100)
    userUid: str = Field(...)
    createdAt: datetime = Field(...)
    isProfile: bool = Field(False)