from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.database import database
from models.homework import homeworks_table, listeners_homeworks_table
from utils import convertor
from schemas import homework as homework_schema

import pandas as pd

router = APIRouter()

# Получение всей информации из таблицы для курса
@router.get('/getHomeworksbyCourse/{course_id}')
async def get_homeworks(request: Request, course_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
                SELECT id, name, link, percent, to_char(end_date, 'DD.MM.YYYY') AS end_date, course_id
                from {homeworks_table}
                where course_id={course_id}"""  
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


# Получение заданий, которые еще доступны дня добавления по дате
@router.get('/getAvailableHomework/{course_id}')
async def get_available_homeworks(request: Request, course_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
                SELECT id, name
                from {homeworks_table}
                where course_id={course_id} and end_date > current_date"""  
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


# Добавление задания
@router.post('/addHomework/')
async def add_homework(request: Request, homework: homework_schema.AddHomework):
    
    try:
        query = homeworks_table.insert().values(name=homework.name, end_date=homework.end_date, link=homework.link, percent=homework.percent, course_id=homework.course_id)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Course successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)


# Добавление задания на проверку пользователем
@router.post('/addListenerHomework/')
async def add_listener_homework(request: Request, listener_homework: homework_schema.AddListenerHomework):
    
    try:
        query = listeners_homeworks_table.insert().values(link=listener_homework.link, status=listener_homework.status,  homework_id=listener_homework.homework_id, listener_id=listener_homework.listener_id)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Course successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Получение отправленных слушателем заданий
@router.get('/getHomeworksbyListener/{user_id}/{homework_id}/')
async def get_homeworks(request: Request, user_id: int, homework_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
                SELECT listeners_homeworks.id, listeners_homeworks.link, listeners_homeworks.status AS check, listener_id, homework_id, {homeworks_table}.name AS name
                from {listeners_homeworks_table}
                left join {homeworks_table} on {homeworks_table}.id = {listeners_homeworks_table}.homework_id
                where {homeworks_table}.course_id={homework_id} AND {listeners_homeworks_table}.listener_id={user_id}"""  
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

# Получение отправленных слушателем заданий у преподавателя
@router.get('/getAllHomeworks/{id}/')
async def get_homeworks_ny_name(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
                SELECT listeners_homeworks.id, listeners_homeworks.link, listeners_homeworks.status AS check, 
                listener_id, homework_id, {homeworks_table}.name AS name, courses.name as course_name,
                first_name, last_name, patronymic
                from {listeners_homeworks_table}
                left join {homeworks_table} on {homeworks_table}.id = {listeners_homeworks_table}.homework_id
                left join courses on courses.id = homeworks.course_id 
                left join users on users.id = listeners_homeworks.listener_id 
                where listeners_homeworks.status=0 AND courses.tutor_id={id}"""  
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

# Редактирование данных
@router.post('/editListenerHomework/')
async def edit_listener_homework(request: Request, listener_homework: homework_schema.EditListenerHomework):
    
    detail = "Something went wrong"

    try:
        query = listeners_homeworks_table.select().where(listeners_homeworks_table.c.id==listener_homework.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = listeners_homeworks_table.update().where(listeners_homeworks_table.c.id==listener_homework.id).values(link=listener_homework.link, status=listener_homework.status)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Course successfully updated")
        
        else:
            detail = f"Course with id {listener_homework.id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
