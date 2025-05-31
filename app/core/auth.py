from typing import Optional
from passlib.context import CryptContext
from core.settings import Settings
import datetime
import jwt
import os

config = Settings()
SECRET_KEY = config.JWT_SECRET_KEY or os.urandom(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + (expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.DecodeError:
        return None
    
def create_password_reset_token(email: str) -> str:
    to_encode = {"email": email}
    expire_time = datetime.timedelta(minutes=10)
    return create_access_token(to_encode, expire_time)

def decode_password_reset_token(token: str) -> Optional[dict]:
    payload = decode_token(token)
    return payload
