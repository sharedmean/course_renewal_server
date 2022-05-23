from pydantic import UUID4, BaseModel, validator, Field
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class TokenBase(BaseModel):
    token: UUID4 = Field(...,alias='access_token')
    expires: datetime
    token_type: Optional[str] = 'bearer'

    class Config:
        allow_population_by_field_name = True

    @validator('token')
    def hexlify_token(cls, value):\
        return value.hex


class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str
    login: str
    password: str
    role_id: int

    @validator('last_name')
    def check_fitst_name(cls, v):
        if len(v) > 0 and len(v) < 100:
            return v
        else:
            raise ValueError('Некорректные данные')

    @validator('first_name')
    def check_last_name(cls, v):
        if len(v) > 0 and len(v) < 50:
            return v
        else:
            raise ValueError('Некорректные данные')

class UserWithoutPassword(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str
    login: str
    role_id: int

    @validator('last_name')
    def check_fitst_name(cls, v):
        if len(v) > 0 and len(v) < 100:
            return v
        else:
            raise ValueError('Некорректные данные')

    @validator('first_name')
    def check_last_name(cls, v):
        if len(v) > 0 and len(v) < 50:
            return v
        else:
            raise ValueError('Некорректные данные')

class AddUser(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str
    login: str
    password: str
    role_id: int

    @validator('last_name')
    def check_fitst_name(cls, v):
        if len(v) > 0 and len(v) < 100:
            return v
        else:
            raise ValueError('Некорректные данные')

    @validator('first_name')
    def check_last_name(cls, v):
        if len(v) > 0 and len(v) < 50:
            return v
        else:
            raise ValueError('Некорректные данные')


class User(UserBase):
    token: TokenBase = {}
