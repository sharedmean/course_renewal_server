from datetime import date
import arrow
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from numpy import datetime_as_string
from models.database import database
from models.courses import courses_table
from utils import convertor
from schemas import courses as courses_schema

import pandas as pd

router = APIRouter()

# Получение всей информации из таблицы
@router.get('/getCourses')
async def get_courses(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {courses_table}
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
@router.get('/getCourse/{id}')
async def get_course_by_id(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = courses_table.select().where(courses_table.c.id==id)                      # Запрос
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

# Получение всей информации из таблицы
@router.get('/getCoursesByDate')
async def get_courses_by_date(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {courses_table} where start_date > current_date
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

# Получение всех текущих курсов у преподавателя
@router.get('/getCurrentCourseByTutor/{id}')
async def get_courses_by_tutor(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT id, name, hours, price, form, to_char(start_date, 'DD.MM.YYYY') AS start_date, to_char(end_date, 'DD.MM.YYYY') AS end_date, tutor_id, schedule
        FROM {courses_table} WHERE end_date > current_date AND tutor_id={id}
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

# Получение всех завершенных курсов у преподавателя
@router.get('/getFinishedCourseByTutor/{id}')
async def get_finished_courses_by_tutor(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT id, name, hours, price, form, to_char(start_date, 'DD.MM.YYYY') AS start_date, to_char(end_date, 'DD.MM.YYYY') AS end_date, tutor_id, schedule, program
        FROM {courses_table} WHERE end_date < current_date AND tutor_id={id}
        ORDER BY id desc
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

# Получение всех предстоящих курсов
@router.get('/getUpcomingCourses')
async def get_upcoming_courses(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT id, name, hours, price, form, to_char(start_date, 'DD.MM.YYYY') AS start_date, to_char(end_date, 'DD.MM.YYYY') AS end_date, schedule, tutor_id, program
        FROM {courses_table} WHERE end_date > current_date AND start_date > current_date
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

# Получение всех текущих курсов
@router.get('/getCurrentCourses')
async def get_current_courses(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT id, name, hours, price, form, to_char(start_date, 'DD.MM.YYYY') AS start_date, to_char(end_date, 'DD.MM.YYYY') AS end_date, schedule, tutor_id, program
        FROM {courses_table} WHERE end_date > current_date AND start_date <= current_date
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

# Получение всех завершенных курсов
@router.get('/getFinishedCourses')
async def get_finished_courses(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT id, name, hours, price, form, to_char(start_date, 'DD.MM.YYYY') AS start_date, to_char(end_date, 'DD.MM.YYYY') AS end_date, schedule, tutor_id
        FROM {courses_table} WHERE end_date < current_date
        ORDER BY id desc
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

# Добавление данных в таблицу
@router.post('/addCourse/')
async def add_course(request: Request, course: courses_schema.AddCourse):
    
    try:
        query = courses_table.insert().values(name=course.name, hours=course.hours, price=course.price, form=course.form, start_date=course.start_date, end_date=course.end_date, program=course.program, tutor_id=course.tutor_id, schedule=course.schedule)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Course successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Редактирование данных
@router.post('/editCourse/')
async def edit_course(request: Request, course: courses_schema.Course):
    
    detail = "Something went wrong"

    try:
        query = courses_table.select().where(courses_table.c.id==course.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = courses_table.update().where(courses_table.c.id==course.id).values(name=course.name, hours=course.hours, price=course.price, form=course.form, start_date=course.start_date, end_date=course.end_date, program=course.program, tutor_id=course.tutor_id, schedule=course.schedule)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Course successfully updated")
        
        else:
            detail = f"Course with id {course.id} not found"
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
@router.delete('/deleteCourse/{id}/')
async def delete_course(request: Request, id: int):
    
    detail = "Something went wrong"

    try:
        query = courses_table.select().where(courses_table.c.id==id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = courses_table.delete().where(courses_table.c.id==id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Course successfully deleted")
        
        else:
            detail = f"Course with id {id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
