from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME : str
    DATABASE_PORT : str
    DATABASE_USERNAME : str
    DATABASE_PASSWORD : str
    SECRET_KEY : str
    DATABASE_NAME : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    class Config:
        env_file = ".env"


settings = Settings()
