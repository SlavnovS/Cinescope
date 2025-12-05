import os
from dotenv import load_dotenv

load_dotenv()

print("HOST:", os.getenv("DB_MOVIES_HOST"))
print("PORT:", os.getenv("DB_MOVIES_PORT"))
print("URL :", os.getenv("DB_MOVIES_URL"))

class MoviesDataBaseCreds:
    DATABASE_NAME = os.getenv('DB_MOVIES_NAME')
    USERNAME = os.getenv('DB_MOVIES_USERNAME')
    PASSWORD = os.getenv('DB_MOVIES_PASSWORD')
    HOST = os.getenv('DB_MOVIES_HOST')
    PORT = os.getenv('DB_MOVIES_PORT')