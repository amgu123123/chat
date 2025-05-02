from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from schemas.user import UserCreate, UserOut


async def get_user_by_name(db: AsyncSession, name: str) -> UserOut | None:
    stmt = select(User).where(User.username == name)
    result = await db.execute(stmt)
    schema_user = UserOut.model_validate(result.scalar())
    return schema_user


async def create_user(db: AsyncSession, userCreate: UserCreate):
    # todo hash pwd
    user = User(
        username=userCreate.username, hashed_password=userCreate.password
    )
    db.add(user)
    await db.commit()
    return user


async def get_user_by_idset(db: AsyncSession, ids: list[int]) -> list[UserOut]:
    users = []
    for id in ids:
        stmt = select(User).where(User.id == id)
        result = await db.execute(stmt)
        schema_user=UserOut.model_validate(result.scalar())
        users.append(schema_user)
    return users
