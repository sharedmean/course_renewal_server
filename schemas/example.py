from pydantic import BaseModel
from typing import Optional

class Example(BaseModel):
    id: int
    name: str
    params: Optional[str]
    test: Optional[int]

class AddExample(BaseModel):
    name: str
    params: Optional[str]
    test: Optional[int]