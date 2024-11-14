from pydantic import BaseModel

class UserFilter(BaseModel):
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value