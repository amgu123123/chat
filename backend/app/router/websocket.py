from fastapi import HTTPException
from socketio import AsyncServer
from starlette import status

from core.dependencies import get_current_user
from db.crud.message import create_message
from db.session import get_db

from schemas.message import MessageCreate
from service.ConnectionManager import ConnectionManager
from utils.log import logger

sio = AsyncServer(async_mode='asgi', cors_allowed_origins=[])
connectionManager = ConnectionManager(sio)


@sio.event
async def connect(sid, environ, auth):
    try:
        token = auth.get('token')  # 从客户端auth获取token
        async with get_db() as db:
            user = await get_current_user(token, db)  # 验证用户
            # 记录在线用户
            await connectionManager.add_connection(sid, user.id, db)

            logger.info(f"User {user.id} connected with session {sid}")
            await sio.emit('connected', {'status': 'ok'},
                           room=sid)  # 单独响应连接成功
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        await sio.emit('error', {'message': 'Connect failed'}, room=sid)
        await sio.disconnect(sid)


@sio.event
async def disconnect(sid):
    async with get_db() as db:
        uid = await connectionManager.remove_connection(sid, db)
        if uid:
            logger.info(f"User {uid} disconnected from session {sid}")


@sio.on('message:send')
async def message_send(sid, data):
    try:

        logger.info(f'{sid} sent {data}')
        # 从连接池获取用户ID
        uid = connectionManager.active_connections.get(sid, None)
        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="UNAUTHORIZED",
                headers={"WWW-Authenticate": "Bearer"},
            )

        async with get_db() as db:
            msgCreate = MessageCreate(content=data, user_id=uid)
            # 保存到数据库
            msg = await create_message(db, msgCreate)
            # 广播
            await sio.emit('message:new',
                           msg.model_dump_json(),
                           room=None)
    except Exception as e:
        logger.error(f"Send failed: {str(e)}")
        await sio.emit('error', {'message': 'Send failed'}, room=sid)
        await sio.disconnect(sid)
