from fastapi import  HTTPException
from socketio import AsyncServer
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from db.crud.message import create_message, get_message_list
from db.crud.user import get_user_by_idset
from db.session import get_db

from schemas.message import MessageCreate

sio = AsyncServer(async_mode='asgi', cors_allowed_origins=[])
active_connections = {}

async def update_online_user(db:AsyncSession):
    id_set = list(set(active_connections.values()))
    online_users = await get_user_by_idset(db, id_set)
    json_str = [user.model_dump_json() for user in online_users]

    await sio.emit('user_online',
                   json_str,
                   room=None)

@sio.event
async def connect(sid, environ, auth):
    try:
        print(f'{sid} connect success')
        token = auth.get('token')  # 从客户端auth获取token
        db_gen = get_db()
        db = await anext(db_gen)
        user = await get_current_user(token, db)  # 验证用户

        active_connections[sid] = user.id  # 记录在线用户
        # 全局（room = None）
        # 更新在线用户列表
        await update_online_user(db)
        await sio.emit('connected', {'status': 'ok'},
                       room=sid)  # 单独响应连接成功
    except Exception as e:
        print("err",e)
        await sio.emit('error', {'message': str(e)}, room=sid)
        await sio.disconnect(sid)


@sio.event
async def disconnect(sid):
    uid = active_connections.pop(sid, None)
    if uid:
        # 更新用户在线状态
        db_gen = get_db()
        db = await anext(db_gen)
        await update_online_user(db)


@sio.on('message:send')
async def message_send(sid, data):
    try:
        print(f'{sid} sent {data}')
        uid = active_connections.get(sid, None)
        if not uid:
            raise HTTPException(status_code=400,
                                detail="insert message fail")
        msgCreate = MessageCreate(content=data, user_id=uid)
        db_gen = get_db()
        db = await anext(db_gen)
        # 保存到数据库
        msg = await create_message(db, msgCreate)

        # 这里可以添加消息处理逻辑
        if not msg:
            raise HTTPException(status_code=400,
                                detail="insert message fail")

        # 广播
        await sio.emit('message:new',
                       msg.model_dump_json(),
                       room=None)
    except Exception as e:
        await sio.emit('error', {'message': str(e)}, room=sid)
