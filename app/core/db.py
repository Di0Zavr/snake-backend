from sqlmodel import SQLModel, create_engine, Session
from core.settings import Settings
from models.models import *
import psycopg2

config = Settings()

DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

def get_db_session():
    with Session(engine) as session:
        yield session