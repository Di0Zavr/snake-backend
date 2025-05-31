from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import datetime

class UserRegistration(BaseModel):
    username: str = Field(
        min_length=8,
        pattern=r'^[\w\d_\.]*$'
    )
    email: EmailStr
    password: str
    password_confirm: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserEmailForPasswordReset(BaseModel):
    email: EmailStr

class UserPasswordReset(BaseModel):
    reset_token: str
    password: str
    password_confirm: str

class UserPasswordChange(BaseModel):
    password: str
    password_confirm: str

class PasswordResetResponse(BaseModel):
    success: bool

class UserResponse(BaseModel):
    id: int
    username: str = Field(
        min_length=8,
        pattern=r'^[\w\d_\.]*$'
    )
    email: EmailStr
    created_at: datetime.datetime
    last_login: Optional[datetime.datetime] = None

class PasswordTokenResponse(BaseModel):
    token: str

class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"