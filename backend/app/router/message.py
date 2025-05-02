from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from db.crud.message import get_message_list
from db.session import get_db
from schemas.message import MessageOut
from schemas.user import UserOut

router = APIRouter()


@router.get("", response_model=list[MessageOut])
async def get_list(skip: int = 0,
                   limit: int = 100,
                   current_user: UserOut = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    message_list = await get_message_list(db,skip=skip,limit=limit)
    return message_list
