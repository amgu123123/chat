import socketio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from db.session import init_db
from db import models  # 重要，不能删掉
from router import auth, message
from router.websocket import sio

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(auth.router, prefix='/api/auth', tags=['auth'])
app.include_router(message.router, prefix='/api/message', tags=['message'])

# # 核心配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 必须精确匹配
    allow_credentials=True,  # 如果需要认证
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_db()
# 挂载 Socket.IO 到 FastAPI
app.mount("/", socketio.ASGIApp(sio))




