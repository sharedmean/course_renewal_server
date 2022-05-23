from tokenize import String
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.database import database
from models.documents import documents_table
from utils import convertor
from schemas import documents as document_schema

import pandas as pd

router = APIRouter()

# Получение всех документов в статусе "в ожидании проверки"
@router.get('/getAllDocsStatus0')
async def get_docs_status0(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        select users.first_name as first_name, users.last_name as last_name, users.patronymic as patronymic, 
        documents.link as link, documents.name as name, documents.id as id, users.id as user_id
        from documents
        left join users 
        on users.id = documents.user_id 
        where documents.status = 0
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
@router.get('/getDocsId/{id}')
async def get_docs_by_id(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = documents_table.select().where(documents_table.c.id==id)                      # Запрос
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

# Получение всей информации из таблицы по user_id
@router.get('/getDocsUser/{user_id}')
async def get_docs_by_user_id(request: Request, user_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {documents_table} WHERE user_id={user_id}
        ORDER BY id DESC
        """
        result = await database.fetch_all(query)                                          # Выполнение запроса

        # Если в таблице нет данных
        if not result:
            detail = "Data not found"
        else:
            # Преобразуем в JSON с помощью нашего конвертора из папки utils и возвращаем
            return convertor.dataframe_to_json(pd.DataFrame(result))
    
    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Data not found":
            return convertor.dataframe_to_json(pd.DataFrame(0))
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)

# Добавление данных в таблицу
@router.post('/addDoc/')
async def add_doc(request: Request, doc: document_schema.AddDocument):
    
    try:
        query = documents_table.insert().values(name=doc.name, link=doc.link, status=doc.status, user_id=doc.user_id)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Document successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Редактирование данных
@router.post('/editDoc/')
async def edit_doc(request: Request, doc: document_schema.Document):
    
    detail = "Something went wrong"

    try:
        query = documents_table.select().where(documents_table.c.id==doc.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = documents_table.update().where(documents_table.c.id==doc.id).values(name=doc.name, link=doc.link, status=doc.status, user_id=doc.user_id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Document successfully updated")
        
        else:
            detail = f"Document with id {doc.id} not found"
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
@router.delete('/deleteDoc/{id}')
async def delete_doc(request: Request, id: int):
    
    detail = "Something went wrong"

    try:
        query = documents_table.select().where(documents_table.c.id==id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = documents_table.delete().where(documents_table.c.id==id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Document successfully deleted")
        
        else:
            detail = f"Document with id {id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
