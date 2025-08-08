import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    SECRET_KEY_ACCESS: str = os.getenv("SECRET_KEY_ACCESS", str(os.urandom(32)))
    SECRET_KEY_REFRESH: str = os.getenv("SECRET_KEY_REFRESH", str(os.urandom(32)))
    JWT_SIGNING_ALGORITHM: str = os.getenv("JWT_SIGNING_ALGORITHM", "HS256")
    LOGIN_TIME_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
