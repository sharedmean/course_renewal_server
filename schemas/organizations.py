from pydantic import BaseModel
from typing import Optional

class Organization(BaseModel):
    id: int
    name: str
    director: str
    phone: str
    email: str

class AddOrganization(BaseModel):
    name: str
    director: str
    phone: str
    email: str