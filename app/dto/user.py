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

class UserPasswordChange(BaseModel):
    password: str
    password_confirm: str

class UserResponse(BaseModel):
    id: int
    username: str = Field(
        min_length=8,
        pattern=r'^[\w\d_\.]*$'
    )
    email: EmailStr
    created_at: datetime.datetime
    last_login: Optional[datetime.datetime] = None

class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"