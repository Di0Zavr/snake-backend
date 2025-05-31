from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import datetime

class User(SQLModel, table=True):
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    username: str = Field(
        unique=True
    )

    email: str = Field(
        unique=True
    )

    password_hash: str

    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )

    last_login: Optional[datetime.datetime] = None

    games: List["GameSession"] = Relationship(
        back_populates="user"
    )

class GameSession(SQLModel, table=True):
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(
        foreign_key="user.id"
    )

    score: int

    duration: int

    moves: Optional[str] = None

    played_at: datetime.datetime

    user: Optional["User"] = Relationship(
        back_populates="games"
    )