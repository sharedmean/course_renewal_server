from datetime import date
from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    id: int
    name: str
    hours: int
    price: float
    form: str
    start_date: date
    end_date: date
    program: str
    tutor_id: int
    schedule: str

class AddCourse(BaseModel):
    name: str
    hours: int
    price: float
    form: str
    start_date: date
    end_date: date
    program: str
    tutor_id: int
    schedule: str