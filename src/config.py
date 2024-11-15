from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URL: Optional[str] = None
    JWT_SECRET:Optional[str] = None
    JWT_ALGORITHM:Optional[str] = None
    REDIS_HOST:str = "localhost"
    REDIS_PORT:int = 6379
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    GOOGLE_CLIENT_ID:Optional[str] = None
    GOOGLE_CLIENT_SECRET:Optional[str] = None
    SECRET_KEY:Optional[str] = None
    JWT_SECRET_KEY:Optional[str] = None
    

Config = Settings()  # This will automatically load the .env variables
