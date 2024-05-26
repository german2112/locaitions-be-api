from pydantic import BaseModel

class CreateLiveStreamDTO(BaseModel):
    eventId: str
    username: str
    createdBy: str
    photoUrl: str

    def to_dict(self):
        return self.dict(exclude_unset=True)
