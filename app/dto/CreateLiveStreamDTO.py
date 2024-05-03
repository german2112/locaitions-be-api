from pydantic import BaseModel

class CreateLiveStreamDTO(BaseModel):
    eventId: str
    username: str
    createdBy: str

    def to_dict(self):
        self.to_dict()