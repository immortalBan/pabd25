from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    admin_password: str
    
    class Config:
        env_file = ".env"


SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
settings = Settings(database_url=DATABASE_URL, secret_key=SECRET_KEY, admin_password=ADMIN_PASSWORD)