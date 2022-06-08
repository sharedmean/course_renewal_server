from lib2to3.pgen2.pgen import generate_grammar
from tokenize import generate_tokens
from routers import example
from routers import roles
from routers import users
from routers import documents
from routers import courses
from routers import listeners_courses
from routers import agreements
from routers import invoices
from routers import listeners_agreements
from routers import organizations
from routers import homework
from fastapi.middleware.cors import CORSMiddleware
from models.database import database
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)


import os

from fastapi import FastAPI 
from fastapi import FastAPI, File, UploadFile, FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import string
import secrets


import uvicorn
import config

app = FastAPI(docs_url=None, redoc_url=None, root_path=config.API_URL_PREFIX)

app.add_middleware(
    CORSMiddleware,
    allow_origins = config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Подключение к БД
@app.on_event("startup")
async def startup():
    await database.connect()

# Отключение от БД
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Swagger
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=config.STATICFILES_URL_PREFIX + app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url=f"{config.STATICFILES_URL_PREFIX}/static/redoc.standalone.js",
    )


# files stuff

def delete_file(name):
    os.remove(name)

@app.get("/delete")
async def delete(name: str):
    delete_file("files/"+name)
    return name

def save_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)
        print('file saved')

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    print(file)
    contents = await file.read()
    name= ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(20)) 
    name= name+'.pdf'
    save_file("files/"+name, contents)
    return name

@app.get("/download")
async def download(name: str): 
    return FileResponse(
                "files/"+name,
                media_type="application/pdf",
                filename=name)
    #path = "files/"+ name 
    #return FileResponse(path, media_type='application/pdf',filename=name)

# Роутеры
app.include_router(example.router, prefix=config.EXAMPLE_PREFIX, tags=['example'])
app.include_router(roles.router, prefix=config.ROLES_PREFIX, tags=['roles'])
app.include_router(users.router, prefix=config.USERS_PREFIX, tags=['users'])
app.include_router(documents.router, prefix=config.DOCS_PREFIX, tags=['documents'])
app.include_router(courses.router, prefix=config.COURSES_PREFIX, tags=['courses'])
app.include_router(listeners_courses.router, prefix=config.LISTENERS_COURSES_PREFIX, tags=['listeners_courses'])
app.include_router(agreements.router, prefix=config.AGREEMENTS_PREFIX, tags=['agreements'])
app.include_router(invoices.router, prefix=config.INVOICES_PREFIX, tags=['invoices'])
app.include_router(listeners_agreements.router, prefix=config.LISTENERS_AGREEMENTS_PREFIX, tags=['listeners_agreements'])
app.include_router(organizations.router, prefix=config.ORGANIZATIONS_PREFIX, tags=['organizations'])
app.include_router(homework.router, prefix=config.HOMEWORKS_PREFIX, tags=['homeworks'])

# Запуск приложения
if __name__ == '__main__':
    uvicorn.run('main:app', host=config.UVICORN_HOST,
                            port=config.UVICORN_PORT,
                            reload=config.UVICORN_RELOAD)