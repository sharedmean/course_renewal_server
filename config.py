from os import environ

TESTING = environ.get('TESTING', True)

TEMP_FOLDER = 'temp'

#### APP ####

APP_NAME = 'dpo'
APP_VERSION = '1.0.0'

UVICORN_HOST = '127.0.0.1'
UVICORN_PORT = 8000
UVICORN_RELOAD = True

API_URL_PREFIX = ''
STATICFILES_URL_PREFIX = ''

EXAMPLE_PREFIX = '/example'
USERS_PREFIX = '/users'
ROLES_PREFIX = '/roles'
DOCS_PREFIX = '/docs'
COURSES_PREFIX = '/courses'
LISTENERS_COURSES_PREFIX = '/listeners_courses'
AGREEMENTS_PREFIX = '/agreements'
INVOICES_PREFIX = '/invoices'
LISTENERS_AGREEMENTS_PREFIX = '/listeners_agreements'
ORGANIZATIONS_PREFIX = '/organizations'

#### CORS ####

CORS_ORIGINS = [
    'http://localhost',
    'http://localhost:8081',
    'http://localhost:8000'
]

#### DB ####

DB_NAME = environ.get("DB_NAME", 'DPO')
DB_USER = environ.get('DB_USER', 'postgres') 
DB_PASSWORD = environ.get('DB_PASSWORD', '123')
DB_HOST = environ.get('DB_HOST', '127.0.0.1')