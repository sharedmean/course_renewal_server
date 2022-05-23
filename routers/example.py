from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.database import database
from models.example import example_table
from utils import convertor
from schemas import example as example_schema

import pandas as pd

router = APIRouter()

# Получение всей информации из таблицы
@router.get('/getExample')
async def get_example(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = example_table.select()                      # Запрос
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
@router.get('/getExample/{id}')
async def get_example_by_id(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = example_table.select().where(example_table.c.id==id)                      # Запрос
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
@router.post('/addExample/')
async def add_example(request: Request, example: example_schema.AddExample):
    
    try:
        query = example_table.insert().values(name=example.name, params=example.params, test=example.test)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Example successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Редактирование данных
@router.post('/editExample/')
async def edit_example(request: Request, example: example_schema.Example):
    
    detail = "Something went wrong"

    try:
        query = example_table.select().where(example_table.c.id==example.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = example_table.update().where(example_table.c.id==example.id).values(name=example.name, params=example.params, test=example.test)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Example successfully updated")
        
        else:
            detail = f"Example with id {example.id} not found"
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
@router.delete('/deleteExample/{id}')
async def delete_example(request: Request, id: int):
    
    detail = "Something went wrong"

    try:
        query = example_table.select().where(example_table.c.id==id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = example_table.delete().where(example_table.c.id==id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Example successfully deleted")
        
        else:
            detail = f"Example with id {id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
