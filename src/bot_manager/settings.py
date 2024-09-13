import os

from dotenv import load_dotenv

if not os.getenv('IS_DOCKER', False):
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_MANAGER_TOKEN')
API_URL = os.getenv('API_URL')
