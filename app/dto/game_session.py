from pydantic import BaseModel
from typing import Optional
import datetime

class GameSessionCreate(BaseModel):
    score: int
    duration: int
    moves: Optional[str] = None
    played_at: datetime.datetime

class GameSessionResponse(BaseModel):
    id: int
    user_id: int
    score: int
    duration: int
    moves: Optional[str] = None
    played_at: datetime.datetime

class GameSessionTopResponse(BaseModel):
    username: Optional[str] = None
    score: Optional[int] = None