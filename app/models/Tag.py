from pydantic import BaseModel, Field
from datetime import datetime, UTC

class TagSchema(BaseModel):
    label: str
    created_at: datetime = Field(default=datetime.now(UTC))
    event_id: str

    def to_dict(self):
        tagDict = self.dict()
        tagDict['created_at'] = str(self.created_at)
        return tagDict