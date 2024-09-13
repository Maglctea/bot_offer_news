import os

from dotenv import load_dotenv

if not os.getenv('IS_DOCKER', False):
    load_dotenv()

# Aiohttp (for bot webhook)
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBHOOK_SECRET_KEY = os.getenv('SECRET_KEY')

# Database
DB_TYPE = os.getenv('DB_TYPE')
DB_DRIVER = os.getenv('POSTGRES_DRIVER')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB')
API_URL = os.getenv('API_URL')

# API
PATH_TO_STATIC_DIR = os.getenv('PATH_TO_STATIC_DIR')
