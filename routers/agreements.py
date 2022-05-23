from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.database import database
from models.agreements import agreements_table
from utils import convertor
from schemas import agreements as agreements_schema

import pandas as pd

router = APIRouter()

# Получение всей информации из таблицы
@router.get('/getAgreements')
async def get_agreements(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {agreements_table} 
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
@router.get('/getAgreement/{id}')
async def get_agreement_by_id(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = agreements_table.select().where(agreements_table.c.id==id)                      # Запрос
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

# Получение всей информации из таблицы по organization_id
@router.get('/getAgreementByOrganization/{id}')
async def get_agreement_by_organization(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
                SELECT agreements.id AS agreement_id, invoices.amount AS amount, courses.id, invoices.id AS invoice_id, 
                invoices.status AS invoice_status, agreements.status AS status, courses.name, CAST(courses.start_date AS TEXT), 
                agreements.link AS agreements_link,  invoices.link AS invoices_link
                from {agreements_table}
                left join courses on courses.id=agreements.course_id 
                left outer join invoices on invoices.agreement_id=agreements.id
                where agreements.organization_id={id}  
                ORDER BY agreement_id desc"""                        # Запрос
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
@router.post('/addAgreement/')
async def add_agreement(request: Request, agreement: agreements_schema.AddAgreement):
    
    try:
        query = agreements_table.insert().values(link=agreement.link, status=agreement.status, organization_id=agreement.organization_id, course_id=agreement.course_id, partnership_agreement_id=agreement.partnership_agreement_id)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Agreement successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Редактирование данных
@router.post('/editAgreement/')
async def edit_agreement(request: Request, agreement: agreements_schema.Agreement):
    
    detail = "Something went wrong"

    try:
        query = agreements_table.select().where(agreements_table.c.id==agreement.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = agreements_table.update().where(agreements_table.c.id==agreement.id).values(link=agreement.link, status=agreement.status, organization_id=agreement.organization_id, course_id=agreement.course_id, partnership_agreement_id=agreement.partnership_agreement_id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Agreement successfully updated")
        
        else:
            detail = f"Agreement with id {agreement.id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
