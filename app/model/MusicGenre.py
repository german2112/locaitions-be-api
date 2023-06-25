from pydantic import BaseModel, Field

class MusicGenreSchema(BaseModel):
    name: str = Field(..., max_length=40)