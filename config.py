import os
import pathlib
from dotenv import load_dotenv


TOKEN = os.environ.get('token')
BASE_DIR = pathlib.Path(__file__).parent
API_KEY = os.environ.get('api_key')

load_dotenv(BASE_DIR / '.env')

DATABASE_URI = f"mysql+mysqlconnector://{os.getenv('mysql_user')}:{os.getenv('mysql_password')}@localhost/{os.getenv('db_name')}"
