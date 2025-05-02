from pydantic import BaseModel


class Settings(BaseModel):
    PROJECT_NAME: str = "Chat"
    SECRET_KEY: str = '123ASDgqm'
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30mins
    DATABASE_URL: str = 'postgresql+asyncpg://postgres:123456@localhost:5432/chat'

    class Config:
        case_sensitive = True


settings = Settings()
