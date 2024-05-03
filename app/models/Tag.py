from pydantic import BaseModel, Field
from datetime import datetime

class Tag(BaseModel):
    label: str
    created_at: datetime = Field(default=datetime.utcnow())
    event_id: str