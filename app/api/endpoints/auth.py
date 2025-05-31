from fastapi import APIRouter, Depends, HTTPException
from dto.user import UserRegistration, UserLogin, UserResponse, TokenResponse
from core.auth import create_access_token, hash_password, verify_password
from core.db import get_db_connection, get_db_session
from models.models import User
import datetime

auth_router = APIRouter()

@auth_router.post("/dummyLogin",
                  response_model=TokenResponse,
                  summary="Получение тестового токена"
                  )
def dummyLogin():
    token = create_access_token(
        data={"id": 1}
    )
    return TokenResponse(token=token)

@auth_router.post("/register",
                  response_model=UserResponse,
                  summary="Регистрация пользователя"
                  )
def register(data: UserRegistration, conn=Depends(get_db_connection)):
    cursor = conn.cursor()

    if data.password != data.password_confirm:
        raise HTTPException(
            status_code=400,
            detail="Пароли не совпадают"
        )

    cursor.execute(
        """
        SELECT id FROM \"user\"
        WHERE email = %s
        OR username = %s
        """,
        (data.email, data.username)
    )

    if cursor.fetchone():
        raise HTTPException(
            status_code=400,
            detail="Email или имя пользователя уже существует"
        )

    cursor.execute(
        """
        INSERT INTO \"user\" (username, email, password_hash, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (data.username, data.email, hash_password(data.password), datetime.datetime.now(datetime.UTC))
    )
    conn.commit()

    cursor.execute(
        """
        SELECT id, created_at FROM \"user\"
        WHERE username = %s
        """,
        (data.username,)
    )
    result = cursor.fetchone()
    id, created_at = result

    user = UserResponse(
        id=id,
        username=data.username,
        email=data.email,
        created_at=created_at,
        last_login=None
    )
    
    return user

@auth_router.post("/login",
                  response_model=TokenResponse,
                  summary="Авторизация пользователя"
                  )
def login(data: UserLogin, conn=Depends(get_db_connection)):
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, password_hash from \"user\"
        WHERE email = %s
        """,
        (data.email,)
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Неверные учетные данные"
        )
    
    id, hashed_password = result
    if not verify_password(data.password, hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Неверные учетные данные"
        )

    last_login = datetime.datetime.now(datetime.UTC)
    cursor.execute(
        """
        UPDATE \"user\"
        SET last_login=%s
        WHERE email=%s
        """,
        (last_login, data.email)
    )
    conn.commit()
    
    token = create_access_token(
        data={"id": id}
    )
    
    return TokenResponse(token=token)
