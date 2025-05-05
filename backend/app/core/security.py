from datetime import timedelta, datetime, timezone
from typing import Literal

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.exceptions import TokenExpiredError, TokenDecodeError, \
    TokenTypeMismatchError
from db.crud.user import get_user_by_name
from schemas.user import UserOut
from utils.log import logger

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


def create_token(type: Literal["access", "refresh"], username: str):
    if type=="refresh":
        secret_key=settings.REFRESH_SECRET_KEY
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    elif type=="access":
        secret_key = settings.ACCESS_SECRET_KEY
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": username}
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({"exp": expire, "type": type})
    encoded_jwt = jwt.encode(data, secret_key,
                             algorithm=settings.ALGORITHM)
    return encoded_jwt




def verify_token(token: str,type: Literal["access", "refresh"])->dict:
    if type=="refresh":
        secret_key=settings.REFRESH_SECRET_KEY
    elif type=="access":
        secret_key = settings.ACCESS_SECRET_KEY
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != type:
            logger.debug("token type error")
            raise TokenTypeMismatchError()
        return payload
    except ExpiredSignatureError:
        logger.debug("token expire")
        raise TokenExpiredError()
    except JWTError as e:
        logger.debug(f"JWT解析错误: {str(e)}")
        raise TokenDecodeError(f"JWT解析错误: {str(e)}")
