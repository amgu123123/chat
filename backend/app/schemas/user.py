from datetime import datetime

from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    # email: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(User):
    created_at: datetime
    avatar:str|None
    class Config:
        from_attributes = True  # 允许ORM模型转换

        json_encoders = {
            datetime: lambda dt: dt.isoformat()  # 自动处理 datetime
        }
