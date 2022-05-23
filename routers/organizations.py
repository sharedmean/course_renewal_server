from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.database import database
from models.organizations import organizations_table
from utils import convertor
from schemas import organizations as organization_schema

import pandas as pd

router = APIRouter()

# Получение всей информации из таблицы
@router.get('/getOrganizations')
async def get_organizations(request: Request):
    
    detail = "Something went wrong"
    
    try:
        query = f"""
        SELECT * FROM {organizations_table} WHERE id<>0 ORDER BY id DESC
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
@router.get('/getOrganization/{id}')
async def get_organization_by_id(request: Request, id: int):
    
    detail = "Something went wrong"
    
    try:
        query = organizations_table.select().where(organizations_table.c.id==id)                      # Запрос
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
@router.post('/addOrganization/')
async def add_organization(request: Request, organization: organization_schema.AddOrganization):
    
    try:
        query = organizations_table.insert().values(name=organization.name, director=organization.director, phone=organization.phone, email=organization.email)  # Запрос
        await database.execute(query)                                                                       # Выполнение запроса

        return JSONResponse(status_code=200, content="Organization successfully added")

    # Обработка ошибок
    except Exception as exception:
        raise HTTPException(status_code=404,detail=exception)

# Редактирование данных
@router.post('/editOrganization/')
async def edit_organization(request: Request, organization: organization_schema.Organization):
    
    detail = "Something went wrong"

    try:
        query = organizations_table.select().where(organizations_table.c.id==organization.id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = organizations_table.update().where(organizations_table.c.id==organization.id).values(name=organization.name, director=organization.director, phone=organization.phone, email=organization.email)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Organization successfully updated")
        
        else:
            detail = f"Organization with id {organization.id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)

# Удаление организации
@router.delete('/deleteOrganization/{id}')
async def delete_user(request: Request, id: int):
    
    detail = "Something went wrong"

    try:
        query = organizations_table.select().where(organizations_table.c.id==id)
        ifExist = await database.fetch_all(query)

        if ifExist:
            query = organizations_table.delete().where(organizations_table.c.id==id)
            await database.execute(query)

            return JSONResponse(status_code=200, content="Organization successfully deleted")
        
        else:
            detail = f"Organization with id {id} not found"
            raise HTTPException(status_code=404, detail=detail)

    # Обработка ошибок
    except Exception as exception:
        # Если неизвестная ошибка
        if detail == "Something went wrong":
            raise HTTPException(status_code=404,detail=exception)
        
        # Если обработанная ошибка
        else:
            raise HTTPException(status_code=404,detail=detail)
