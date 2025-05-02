from datetime import timedelta, datetime, timezone
from typing import Union

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.crud.user import get_user_by_name
from schemas.user import UserOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(db: AsyncSession, username: str,
                            password: str) -> UserOut | None:
    user = await get_user_by_name(db, username)
    if not user:
        return None

    # TODO 添加密码验证逻辑
    # if not verify_password(password, user.hashed_password):
    #     return None
    return user


def create_access_token(username: str,
                        expires_delta: Union[timedelta, None] = None):
    data = {"sub": username}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM)
    return encoded_jwt
