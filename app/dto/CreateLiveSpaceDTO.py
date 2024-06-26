from pydantic import BaseModel

class CreateLiveSpaceDTO(BaseModel):
    eventId: str
    username: str
    createdBy: str
    photoUrl: str
    agoraChatUser: str

    def to_dict(self):
        return self.dict(exclude_unset=True)
