from fastapi import FastAPI
from core.db import init_db
from api.endpoints.auth import auth_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"Hello": "world"}

app.include_router(auth_router)