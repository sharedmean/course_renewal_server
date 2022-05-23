from pydantic import BaseModel
from typing import Optional

class Role(BaseModel):
    id: int
    details: str

class AddRole(BaseModel):
    details: str
    