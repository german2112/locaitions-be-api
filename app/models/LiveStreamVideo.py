from pydantic import BaseModel
from pydantic import Field

class LiveStreamVideoSchema(BaseModel):
    id: str = Field(default=None)
    createdBy: str
    eventId: str
    channelId: str
    createdAt: str
    photoUrl: str

    def to_dict(self):
        liveStreamVideoDict = self.dict(exclude_unset=True)
        liveStreamVideoDict["createdAt"] = str(self.createdAt)
        return liveStreamVideoDict