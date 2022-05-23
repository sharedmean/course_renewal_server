from pydantic import BaseModel
from typing import Optional

class Document(BaseModel):
    id: int
    name: str
    link: str
    status: int
    user_id: int

class AddDocument(BaseModel):
    name: str
    link: str
    status: int
    user_id: int