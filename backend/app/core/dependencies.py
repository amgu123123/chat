# 全局依赖项
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.exc import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.config import settings
from db.crud.user import get_user_by_name
from db.session import get_db
from schemas.user import UserOut

# 定义 Token 的获取方式（默认从 `Authorization: Bearer <token>` 获取）
# tokenUrl="token" 表示客户端应该向 api/auth/login 发送用户名和密码来获取 Token。
# 默认情况下，Token 会从请求头的 Authorization: Bearer <token> 中提取。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: AsyncSession = Depends(get_db)) -> UserOut:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError as e:
        raise credentials_exception
    user = await get_user_by_name(db, username)
    if not user:
        raise credentials_exception
    return UserOut.model_validate(user)


