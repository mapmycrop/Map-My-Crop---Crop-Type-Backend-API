from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    SERVER: str
    LOGO: str
    ENVIRONMENT: str
    FRONTEND_LINK: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASSWORD: str
    DB_USER: str

    DATA_DB_HOST: str
    DATA_DB_PORT: int
    DATA_DB_NAME: str
    DATA_DB_PASSWORD: str
    DATA_DB_USER: str

    REDIS_HOST: str
    REDIS_PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_HOUR: int

    SENDINBLUE_KEY: str

    class Config:
        env_file = Path(Path(__file__).resolve().parent) / ".env"


setting = Settings()
