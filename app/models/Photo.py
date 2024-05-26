from pydantic import BaseModel

class PhotoSchema(BaseModel):
    id: str
    filename: str
    fileUrl: str
    createdAt: str
    isProfile: bool

    def to_dict(self):
        return self.dict()