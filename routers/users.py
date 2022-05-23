from fastapi import APIRouter, HTTPException, Request, Depends
from utils.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from utils import convertor
from utils import users as users_utils
from models.database import database
from models.users import users_table
from utils import convertor
from schemas import users as user_schema

import pandas as pd

router = APIRouter()

# Аутентификация
@router.post("/auth", response_model=user_schema.TokenBase)
async def auth(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_login(login=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")

    user = convertor.dataframe_to_json(pd.DataFrame(user))['rows'][0]

    if not users_utils.validate_password(
        password=form_data.password, password_hash=user["password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect login or password")

    return await users_utils.create_user_token(user_id=user["id"])

# Информация о текущем пользователе
@router.get("/me")
async def about_me(current_user: user_schema.User = Depends(get_current_user)):
    return current_user

# Получение всех пользователей
@router.get('/getUsers')
async def get_users(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {users_table} ORDER BY id DESC
        """
        result = await database.fetch_all(query)            # Выполнение запроса

        # Если в таблице нет данных
        if not result:
            detail = "Data not found"
            raise HTTPException(status_code=404, detail=detail)
        else:
            # Преобразуем в JSON с помощью нашего конвертора из папки utils и возвращаем
            return convertor.dataframe_to_json(pd.DataFrame(result))
    
    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)

# Получение всех преподавателей
@router.get('/getTutors')
async def get_tutors(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT id, concat(last_name, ' ', first_name, ' ', patronymic) as name FROM {users_table} WHERE role_id=2 ORDER BY id DESC
        """
        result = await database.fetch_all(query)            # Выполнение запроса

        # Если в таблице нет данных
        if not result:
            detail = "Data not found"
            raise HTTPException(status_code=404, detail=detail)
        else:
            # Преобразуем в JSON с помощью нашего конвертора из папки utils и возвращаем
            return convertor.dataframe_to_json(pd.DataFrame(result))
    
    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)

# Получение всей информации из таблицы по id
@router.get('/getUser/{id}')
async def get_user_by_id(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = users_table.select().where(users_table.c.id==id)                      # Запрос
        result = await database.fetch_all(query)                                          # Выполнение запроса

        # Если в таблице нет данных
        if not result:
            detail = "Data not found"
            raise HTTPException(status_code=404, detail=detail)
        else:
            # Преобразуем в JSON с помощью нашего конвертора из папки utils и возвращаем
            return convertor.dataframe_to_json(pd.DataFrame(result))
    
    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)

# Добавление данных в таблицу
@router.post('/addUser/')
async def add_user(request: Request, user: user_schema.AddUser):
    
    try:
        salt = users_utils.get_random_string()
        hashed_password = users_utils.hash_password(user.password, salt)
        query = users_table.insert().values(first_name=user.first_name, last_name=user.last_name, patronymic=user.patronymic, phone=user.phone, email=user.email, login=user.login, password=f"{salt}${hashed_password}", role_id=user.role_id)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="User successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Редактирование данных
@router.post('/editUser/')
async def edit_user(request: Request, user: user_schema.User):
    
    detail = "Something went wrong"

    try:
        query = users_table.select().where(users_table.c.id==user.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            salt = users_utils.get_random_string()
            hashed_password = users_utils.hash_password(user.password, salt)
            query = users_table.update().where(users_table.c.id==user.id).values(first_name=user.first_name, last_name=user.last_name, patronymic=user.patronymic, phone=user.phone, email=user.email, login=user.login, password=f"{salt}${hashed_password}", role_id=user.role_id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="User successfully updated")
        
        else:
            detail = f"User with id {user.id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)

# Редактирование данных
@router.post('/editUserWithoutPassword/')
async def edit_user(request: Request, user: user_schema.UserWithoutPassword):
    
    detail = "Something went wrong"

    try:
        query = users_table.select().where(users_table.c.id==user.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = users_table.update().where(users_table.c.id==user.id).values(first_name=user.first_name, last_name=user.last_name, patronymic=user.patronymic, phone=user.phone, email=user.email, login=user.login, role_id=user.role_id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="User successfully updated")
        
        else:
            detail = f"User with id {user.id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)

# Удаление пользователя
@router.delete('/deleteUser/{id}')
async def delete_user(request: Request, id: int):
    
    detail = "Something went wrong"

    try:
        query = users_table.select().where(users_table.c.id==id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = users_table.delete().where(users_table.c.id==id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="User successfully deleted")
        
        else:
            detail = f"User with id {id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
