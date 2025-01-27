from os import getenv

from dotenv import load_dotenv

load_dotenv()
DB_HOST = getenv('DB_HOST', 'db')
POSTGRES_DB = getenv('POSTGRES_DB', 'postgres')
POSTGRES_PORT = getenv('POSTGRES_PORT', '5432')
POSTGRES_USER = getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'postgres')
DATABASE_URL = getenv('DATABASE_URL')
