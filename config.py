import os
import pathlib
from dotenv import load_dotenv


BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR / '.env')

TOKEN = os.environ.get('token')
API_KEY = os.environ.get('api_key')

DATABASE_URI = f"mysql+mysqlconnector://{os.getenv('mysql_user')}:{os.getenv('mysql_password')}@localhost/{os.getenv('db_name')}"