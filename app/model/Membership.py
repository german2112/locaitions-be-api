from pydantic import Field, BaseModel

class MembershipSchema(BaseModel):
    type: str = Field(..., max_length=40)
    price: float = Field(..., ge=0)