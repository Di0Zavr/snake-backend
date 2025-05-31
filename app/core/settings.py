from dotenv import load_dotenv
import os

class Settings:
    def __init__(self):
        load_dotenv()
        self.DB_USER = os.getenv("DB_USER") or "postgres"
        self.DB_PASS = os.getenv("DB_PASS") or "postgres"
        self.DB_NAME = os.getenv("DB_NAME") or "snake_db"
        self.DB_PORT = os.getenv("DB_PORT") or "5432"
        self.DB_HOST = os.getenv("DB_HOST") or "localhost"
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or os.urandom(32)
