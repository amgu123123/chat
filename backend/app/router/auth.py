from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.config import settings
from core.dependencies import get_current_user
from core.security import authenticate_user, create_access_token
from db.crud.user import get_user_by_name, create_user
from db.session import get_db
from schemas.user import UserCreate, UserOut

router = APIRouter()


@router.post("/register")
async def register(user_create: UserCreate,
                   db: AsyncSession = Depends(get_db)):
    user = await get_user_by_name(db, user_create.username)
    if user:
        raise HTTPException(status_code=400,
                            detail="name already registered")
    user = await create_user(db, user_create)
    return user


@router.get("/me",response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"})

    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise credentials_exception

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(username,expires_delta=access_token_expires)
        # data={"sub": user.username}, expires_delta=access_token_expires
    # )
    return {"access_token": access_token, "token_type": "bearer","expires_in":settings.ACCESS_TOKEN_EXPIRE_MINUTES*60}
