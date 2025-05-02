from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Message
from schemas.message import MessageCreate, MessageOut


async def create_message(db: AsyncSession,
                         messageCreate: MessageCreate) -> MessageOut:
    message = Message(
        content=messageCreate.content, user_id=messageCreate.user_id
    )
    db.add(message)
    await db.commit()
    stmt = select(Message).where(Message.id == message.id).options(
        selectinload(Message.user))
    result = await db.execute(stmt)
    message_with_user = result.scalar_one()
    return MessageOut(
        id=message_with_user.id,
        content=message_with_user.content,
        created_at=message_with_user.created_at,
        user_id=message_with_user.user_id,
        username=message_with_user.user.username  # 从关联的User对象获取
    )


async def get_message_list(db: AsyncSession, skip: int, limit: int) -> list[
    MessageOut]:
    stmt = (select(Message)
            .offset(skip)
            .limit(limit).order_by(Message.created_at.desc())
            .options(selectinload(Message.user)))
    result = await db.execute(stmt)
    messages = result.scalars()
    messages_list = []
    for message in messages:
        messages_list.append(MessageOut(
            id=message.id,
            content=message.content,
            created_at=message.created_at,
            user_id=message.user_id,
            username=message.user.username  # 从关联的User对象获取
        ))
    return messages_list
