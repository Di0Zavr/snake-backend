from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_current_user_id
from core.auth import hash_password
from core.db import get_db_connection
from dto.user import UserResponse, UserPasswordChange, PasswordResetResponse

user_router = APIRouter()

@user_router.get(
    "/me",
    response_model=UserResponse,
    summary="Получить информацию о текущем пользователе"
)
def get_me(
    conn=Depends(get_db_connection),
    current_user_id=Depends(get_current_user_id)
) -> UserResponse:
    id = current_user_id
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT username, email, created_at, last_login
        FROM \"user\"
        WHERE id = %s
        """,
        (id,)
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    username, email, created_at, last_login = result
    user = UserResponse(
        id=id,
        username=username,
        email=email,
        created_at=created_at,
        last_login=last_login
    )
    return user

@user_router.get(
    "/{id}",
    response_model=UserResponse,
    summary="Получить информацию о пользователе с данным id"
)
def get_user_by_id(
    id: int,
    conn=Depends(get_db_connection),
    current_user_id=Depends(get_current_user_id)
) -> UserResponse:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT username, email, created_at, last_login
        FROM \"user\"
        WHERE id = %s
        """,
        (id,)
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    username, email, created_at, last_login = result
    user = UserResponse(
        id=id,
        username=username,
        email=email,
        created_at=created_at,
        last_login=last_login
    )
    return user

@user_router.post(
    "/change-password",
    response_model=PasswordResetResponse,
    summary="Изменить пароль текущего пользователя"
)
def change_password(
    data: UserPasswordChange,
    conn=Depends(get_db_connection),
    current_user_id=Depends(get_current_user_id)
) -> PasswordResetResponse:
    cursor = conn.cursor()

    if data.password != data.password_confirm:
        raise HTTPException(
            status_code=400,
            detail="Пароли не совпадают"
        )
    
    password_hash = hash_password(data.password)
    cursor.execute(
        """
        UPDATE \"user\"
        SET password_hash = %s
        WHERE id = %s
        """,
        (password_hash, current_user_id)
    )
    conn.commit()
    return PasswordResetResponse(success=True)
    