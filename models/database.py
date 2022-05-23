import config
import databases

DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD
DB_HOST = config.DB_HOST

TESTING = config.TESTING


DB_NAME = 'DPO'
TEST_SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
)
database = databases.Database(TEST_SQLALCHEMY_DATABASE_URL)
