from pydantic import BaseModel
from typing import Optional

class ListenerAgreement(BaseModel):
    user_id: int
    agreement_id: int


class AddListenerAgreement(BaseModel):
    user_id: int
    agreement_id: int