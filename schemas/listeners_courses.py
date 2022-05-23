from pydantic import BaseModel
from typing import Optional

class ListenerCourse(BaseModel):
    id: int
    percent: int
    score: str
    certificate: str
    status: int
    user_id: int
    course_id: int

class AddListenerCourse(BaseModel):
    percent: int
    score: str
    certificate: str
    status: int
    user_id: int
    course_id: int