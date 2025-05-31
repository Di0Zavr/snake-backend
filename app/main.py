from fastapi import FastAPI
from core.db import init_db
from api.endpoints.auth import auth_router
from api.endpoints.user import user_router
from api.endpoints.game_session import game_session_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(game_session_router, prefix="/gamesession", tags=["games"])