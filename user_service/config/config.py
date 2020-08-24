from pydantic import BaseSettings
from pydantic.fields import Field


class Settings(BaseSettings):

    db_dsn: str = Field(env="DB_DSN")
    jwt_phrase: str = Field(env="JWT_PHRASE")

    class Config:
        env_file = ".env"


settings = Settings()
