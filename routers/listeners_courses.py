from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.database import database
from models.listeners_courses import listeners_courses_table
from models.courses import courses_table
from utils import convertor
from schemas import listeners_courses as listener_course_schema

import pandas as pd

router = APIRouter()

# Получение всей информации из таблицы
@router.get('/getListenersCourses')
async def get_listeners_courses(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {listeners_courses_table}
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

# Получение всей информации из таблицы по user_id
@router.get('/getListenerCourseByListener/{user_id}')
async def get_listener_course_by_user_id(request: Request, user_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = listeners_courses_table.select().where(listeners_courses_table.c.user_id==user_id)                      # Запрос
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

# Получение всей информации из таблицы по course_id
@router.get('/getListenerCourseByCourse/{course_id}')
async def get_listener_course_by_course_id(request: Request, course_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {listeners_courses_table} 
        LEFT JOIN users
        ON users.id = listeners_courses.user_id
        WHERE course_id = {course_id} 
        """                  # Запрос
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

# Получение количества студентов по course_id
@router.get('/getCountListenerCourseByCourse/{course_id}')
async def get_count_listener_course_by_course_id(request: Request, course_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT COUNT(user_id) AS listeners_count
        FROM {listeners_courses_table} 
        LEFT JOIN users
        ON users.id = listeners_courses.user_id
        WHERE course_id = {course_id} 
        """                  # Запрос
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

# Получение данных о текущих курсах по user_id
@router.get('/getCurrentCourseByListener/{user_id}')
async def get_current_courses(request: Request, user_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT {courses_table}.name, {courses_table}.program, {listeners_courses_table}.percent, 
        to_char({courses_table}.start_date, 'DD.MM.YYYY') AS start_date, to_char({courses_table}.end_date, 'DD.MM.YYYY') AS end_date, {listeners_courses_table}.user_id, {courses_table}.id
        FROM {listeners_courses_table} 
        LEFT JOIN {courses_table} ON {courses_table}.id={listeners_courses_table}.course_id 
        WHERE {listeners_courses_table}.user_id={user_id} AND {listeners_courses_table}.status=0 
        ORDER BY {courses_table}.id DESC
        """              # Запрос
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

# Получение данных о завершённых курсах по user_id
@router.get('/getFinishedCourseByListener/{user_id}')
async def get_current_courses(request: Request, user_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT {courses_table}.name, {courses_table}.program, {listeners_courses_table}.percent, 
        {listeners_courses_table}.certificate, {listeners_courses_table}.score, {courses_table}.id
        FROM {listeners_courses_table} 
        LEFT JOIN {courses_table} ON {courses_table}.id={listeners_courses_table}.course_id 
        WHERE {listeners_courses_table}.user_id={user_id} AND {listeners_courses_table}.status=1
        ORDER BY {courses_table}.id DESC
        """              # Запрос
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
@router.post('/addListenerCourse/')
async def add_listener_course(request: Request, listener_course: listener_course_schema.AddListenerCourse):
    
    try:
        query = listeners_courses_table.insert().values(percent=listener_course.percent, score=listener_course.score, certificate=listener_course.certificate, status=listener_course.status, course_id=listener_course.course_id, user_id=listener_course.user_id)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="User successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Редактирование данных
@router.post('/editListenerCourse/')
async def edit_listener_course(request: Request, listener_course: listener_course_schema.ListenerCourse):
    
    detail = "Something went wrong"

    try:
        query = listeners_courses_table.select().where(listeners_courses_table.c.id==listener_course.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = listeners_courses_table.update().where(listeners_courses_table.c.id==listeners_courses_table.id).values(percent=listener_course.percent, score=listener_course.score, certificate=listener_course.certificate, status=listener_course.status, course_id=listener_course.course_id, user_id=listener_course.user_id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Listener course successfully updated")
        
        else:
            detail = f"Listener course with id {listener_course.id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
