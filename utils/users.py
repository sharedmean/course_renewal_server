from turtle import position

from fastapi import Query
from models.users import tokens_table, users_table
from schemas import users as user_schema
from datetime import datetime,timedelta
from models.database import database
from sqlalchemy import and_
from utils import convertor

import hashlib
import random
import string

import pandas as pd


# Поиск пользователя по id
async def get_user_by_id(id: int):
    query = users_table.select().where(users_table.c.id == id)
    return await database.execute(query)


# Генерация соли
def get_random_string(length=12):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

# Формирование хеша пароля
def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()

    enc =hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)

    return enc.hex()

# Проверка введенного пароля
def validate_password(password: str, password_hash:str):
    salt, hashed = password_hash.split('$')
    return hash_password(password, salt) == hashed

# Создание токена пользователя
async def create_user_token(user_id: int):
    query = (
        tokens_table.insert()
        .values(expires=datetime.now() + timedelta(hours=8), user_id=user_id)
        .returning(tokens_table.c.token, tokens_table.c.expires)
    )

    return await database.fetch_one(query)
    
# Поиск пользователя по токену
async def get_user_by_token(token: str):

    query = tokens_table.join(users_table).select().where(
        and_(
            tokens_table.c.token == token,
            tokens_table.c.expires > datetime.now()
        )
    )
    return await database.fetch_one(query)

# Поиск пользователя по логину
async def get_user_by_login(login):
    query = users_table.select().where(users_table.c.login == login)
    return await database.fetch_all(query)
