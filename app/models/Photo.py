from pydantic import BaseModel
from datetime import datetime
class PhotoSchema(BaseModel):
    filename: str
    fileUrl: str
    createdAt: datetime
    isProfile: bool

    def to_dict(self):
        return self.__dict__