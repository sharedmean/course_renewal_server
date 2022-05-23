from datetime import date
from pydantic import BaseModel
from typing import Optional

class Invoice(BaseModel):
    id: int
    create_date: date
    end_date: date
    amount: float
    status: int
    link: str
    agreement_id: int

class AddInvoice(BaseModel):
    amount: float
    agreement_id: int

class EditInvoice(BaseModel):
    id: int
    link: str
