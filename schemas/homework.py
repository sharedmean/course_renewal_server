from datetime import date
from pydantic import BaseModel
from typing import Optional

class Homework(BaseModel):
    id: int
    name: str
    link: str
    percent: int
    end_date: date
    course_id: int

class AddHomework(BaseModel):
    name: str
    link: str
    percent: int
    end_date: date
    course_id: int

class AddListenerHomework(BaseModel):
    link: str
    status: int
    homework_id: int
    listener_id: int

class EditListenerHomework(BaseModel):
    id: int
    link: str
    status: int
    