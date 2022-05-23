from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.database import database
from models.invoices import invoices_table
from utils import convertor
from schemas import invoices as invoices_schema

import pandas as pd

router = APIRouter()

# Получение всей информации из таблицы
@router.get('/getInvoices')
async def get_invoices(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {invoices_table}
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
@router.get('/getInvoice/{id}')
async def get_invoice_by_id(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = invoices_table.select().where(invoices_table.c.id==id)                      # Запрос
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
@router.post('/addInvoice/{amount}')
async def add_invoices(request: Request, amount: float):
    
    try:
        query = f"""
        INSERT INTO {invoices_table} (create_date, end_date, amount, status, link, agreement_id) VALUES (current_date, current_date+30, {amount}, 0, '', (select max(id) from agreements))
        """  
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Invoice successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Добавление данных в таблицу
@router.post('/addRenewedInvoice/')
async def add_example(request: Request, invoice: invoices_schema.AddInvoice):
    
    try:
        query = f"""
        INSERT INTO {invoices_table} (create_date, end_date, amount, status, link, agreement_id) VALUES (current_date, current_date+30, {invoice.amount}, 0, '', {invoice.agreement_id})
        """  
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Example successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)


# Редактирование данных
@router.post('/editInvoice/')
async def edit_invoice(request: Request, invoice: invoices_schema.EditInvoice):
    
    
    detail = "Something went wrong"

    try:

        query = invoices_table.select().where(invoices_table.c.id==invoice.id)

        ifExist = await database.fetch_all(query)

        if ifExist:
            
            query = invoices_table.update().where(invoices_table.c.id==invoice.id).values(link = invoice.link)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Invoice successfully updated")
        
        else:
            detail = f"Invoice with id {invoice.id} not found"
            raise HTTPException(status_code=404, detail=detail)
    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
