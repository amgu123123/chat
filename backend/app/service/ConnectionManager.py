from typing import Dict

from socketio import AsyncServer
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.user import get_user_by_idset


class ConnectionManager:
    def __init__(self, sio: AsyncServer):
        self.sio = sio
        self.active_connections: Dict[str, int] = {}

    async def add_connection(self, sid, user_id, db: AsyncSession) -> str:
        self.active_connections[sid] = user_id
        await self.update_online_status(db)

    async def remove_connection(self, sid, db: AsyncSession) -> int:
        user_id = self.active_connections.pop(sid, None)
        if user_id is not None:
            await self.update_online_status(db)
        return user_id

    async def update_online_status(self, db: AsyncSession):
        id_set = list(set(self.active_connections.values()))
        online_users = await get_user_by_idset(db, id_set)
        json_str = [user.model_dump_json() for user in online_users]
        await self.sio.emit('user_online', json_str, room=None)


