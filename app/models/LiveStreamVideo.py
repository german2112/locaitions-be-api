from pydantic import BaseModel
from datetime import datetime
from pydantic import Field

class LiveStreamVideoSchema(BaseModel):
    id: str = Field(default=None)
    createdBy: str
    eventId: str
    channelId: str
    createdAt: datetime

    def to_dict(self):
        liveStreamVideoDict = self.dict(exclude_unset=True)
        liveStreamVideoDict["createdAt"] = str(self.createdAt)
        return liveStreamVideoDict