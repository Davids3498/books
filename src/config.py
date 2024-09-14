from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DB_URL: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

Config = Settings()  # This will automatically load the .env variables
