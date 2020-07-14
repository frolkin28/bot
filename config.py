'''Configuration of the project and global constants'''

import os
import pathlib
from dotenv import load_dotenv


BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR / '.env')

TOKEN = os.getenv('TOKEN')
API_KEY = os.getenv('API_KEY')

DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('IP')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
REDIS_QUEUE_NAME = 'drivers_queue'

redis_config = {
    'host': os.getenv('REDIS_HOST'),
    'port': os.getenv('REDIS_PORT')
}