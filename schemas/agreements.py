from pydantic import BaseModel
from typing import Optional

class Agreement(BaseModel):
    id: int
    link: str
    status: int
    organization_id: int
    course_id: int
    partnership_agreement_id: int

class AddAgreement(BaseModel):
    link: str
    status: int
    organization_id: int
    course_id: int
    partnership_agreement_id: int