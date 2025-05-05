from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "Chat"
    ACCESS_SECRET_KEY: str = 'ACCESS_123ASDgqm'
    REFRESH_SECRET_KEY: str = 'REFRESH_123ASDgqm'
    ALGORITHM: str = "HS256"
    # todo
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 单位：mins
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 单位：day
    DATABASE_URL: str = 'postgresql+asyncpg://postgres:123456@localhost:5432/chat'

    class Config:
        case_sensitive = True


settings = Settings()
