from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.database import database
from models.listeners_agreements import listeners_agreements_table
from models.users import users_table
from models.agreements import agreements_table
from utils import convertor
from schemas import listeners_agreements as listeners_agreements_schema

import pandas as pd

router = APIRouter()

# Получение всей информации из таблицы
@router.get('/getListenersAgreements')
async def get_listeners_agreements(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {listeners_agreements_table}
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
@router.get('/getListenerAgreementByListener/{user_id}')
async def get_listener_agreement_by_user_id(request: Request, user_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
                SELECT agreements.id AS agreement_id, invoices.amount AS amount, courses.id, invoices.id AS invoice_id, 
                invoices.status AS invoice_status, agreements.status AS status, courses.name, CAST(courses.start_date AS TEXT), 
                agreements.link AS agreements_link,  invoices.link AS invoices_link, agreements.organization_id AS organization_id
                from {listeners_agreements_table}
                left join agreements on agreements.id=listeners_agreements.agreement_id  
                left join courses on courses.id=agreements.course_id 
                left outer join invoices on invoices.agreement_id=agreements.id
                where listeners_agreements.user_id={user_id}
                and
                invoices.id=(select max(invoices.id) from invoices where agreement_id=agreements.id)        
                ORDER BY agreement_id DESC"""  
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


# Получение всей информации из таблицы по agreement_id
@router.get('/getListenerAgreementByAgreement/{agreement_id}')
async def get_listener_course_by_course_id(request: Request, agreement_id: int):
    
    detail = "Something went wrong"
    
    try:
        query = listeners_agreements_table.select().where(listeners_agreements_table.c.agreement_id==agreement_id)                      # Запрос
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
@router.post('/addListenerAgreement/{user_id}')
async def add_listener_agreement(request: Request, user_id: int):
    
    try:
        query = f"""
        INSERT INTO {listeners_agreements_table} VALUES ({user_id}, (select max(id) from agreements))
        """  
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Agreement successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)
