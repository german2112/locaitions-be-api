from pydantic import BaseModel, Field

class RoleSchema(BaseModel):
    name: str = Field(..., max_length=40)