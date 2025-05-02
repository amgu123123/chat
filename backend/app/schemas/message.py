from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str
    user_id: int

    class Config:
        from_attributes = True  # 允许ORM模型转换
        json_encoders = {
            datetime: lambda dt: dt.isoformat()  # 自动处理 datetime
        }

class MessageOut(MessageCreate):
    id:int
    username:str
    created_at:datetime
