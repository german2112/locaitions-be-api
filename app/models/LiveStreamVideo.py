from pydantic import BaseModel

class LiveStreamVideoSchema(BaseModel):
    id: str
    createdBy: str
    eventId: str
    channelId: str

    def to_dict(self):
        return self.__dict__