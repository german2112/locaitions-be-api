from pydantic import BaseModel, Field

class ExclusivitySchema(BaseModel):
    name: str = Field(..., max_length=40)