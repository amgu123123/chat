# 全局依赖项
from typing import Annotated

from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security import verify_token
from db.crud.user import get_user_by_name
from db.session import yield_db
from schemas.user import UserOut
from utils.log import logger

# 定义 Token 的获取方式（默认从 `Authorization: Bearer <token>` 获取）
# tokenUrl="token" 表示客户端应该向 api/auth/login 发送用户名和密码来获取 Token。
# 默认情况下，Token 会从请求头的 Authorization: Bearer <token> 中提取。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_user_refresh(grant_type: str = Form(..., regex="refresh_token"),
                           refresh_token: str = Form(...),
                           db: AsyncSession = Depends(yield_db)) -> UserOut:
    """Refresh Token 依赖项"""
    try:
        # 1. 验证基本参数
        if grant_type != "refresh_token":
            raise HTTPException(
                status_code=400,
                detail="Unsupported grant type"
            )
        logger.debug("refresh_token: %s", refresh_token)
        payload = verify_token(refresh_token, "refresh")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token is fail",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return await get_current_user_payload(payload, db)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: AsyncSession = Depends(yield_db)) -> UserOut:
    """Access Token 依赖项"""
    try:
        logger.info("Access_token: %s", token)
        payload = verify_token(token, "access")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="error",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return await get_current_user_payload(payload, db)


async def get_current_user_payload(payload: dict,
                                   db: AsyncSession) -> UserOut:
    username: str | None = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = await get_user_by_name(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return UserOut.model_validate(user)
