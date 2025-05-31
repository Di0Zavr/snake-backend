from fastapi import APIRouter, Depends, HTTPException
from dto.user import UserRegistration, UserLogin, UserResponse, TokenResponse, PasswordTokenResponse, UserEmailForPasswordReset, UserPasswordChange, PasswordResetResponse
from core.auth import create_access_token, hash_password, verify_password, create_password_reset_token, decode_password_reset_token
from core.db import get_db_connection
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

@auth_router.post("/forget-password",
                  response_model=PasswordTokenResponse,
                  summary="Получение токена на восстановление пароля"
                  )
def forget_password(data: UserEmailForPasswordReset, conn=Depends(get_db_connection)):
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, email FROM \"user\"
        WHERE email = %s
        """,
        (data.email,)
    )

    if not cursor.fetchone():
        raise HTTPException(
            status_code=400,
            detail="Неверный email"
        )

    token = create_password_reset_token(data.email)
    return PasswordTokenResponse(token=token)

@auth_router.post("/reset-password",
                  response_model=PasswordResetResponse,
                  summary="Восстановление пароля"
                  )
def reset_password(data: UserPasswordChange, conn=Depends(get_db_connection)):
    payload = decode_password_reset_token(data.reset_token)
    if not payload or not payload.get("email"):
        raise HTTPException(
            status_code=403,
            detail="Неверный токен восстановления пароля"
        )
    
    if data.password != data.password_confirm:
        raise HTTPException(
            status_code=400,
            detail="Пароли не совпадают"
        )
    
    email = payload["email"]
    cursor = conn.cursor()

    password_hash = hash_password(data.password)
    cursor.execute(
        """
        UPDATE \"user\"
        SET password_hash=%s
        WHERE email = %s
        """,
        (password_hash, email)
    )
    conn.commit()

    return PasswordResetResponse(success=True)