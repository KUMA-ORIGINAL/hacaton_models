from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/hacaton_test"
    DB_ECHO: bool = True


settings = Settings()
