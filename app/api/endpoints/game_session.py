from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_current_user_id
from core.db import get_db_connection
from dto.game_session import GameSessionCreate, GameSessionResponse, GameSessionTopResponse
from typing import List

game_session_router = APIRouter()

@game_session_router.post(
    "",
    response_model=GameSessionResponse,
    summary="Создать запись об игровой сессии"
)
def create_game_session(
    data: GameSessionCreate,
    conn=Depends(get_db_connection),
    current_user_id=Depends(get_current_user_id)
) -> GameSessionResponse:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO gamesession (user_id, score, duration, moves, played_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (current_user_id, data.score, data.duration, data.moves, data.played_at)
    )
    conn.commit()

    cursor.execute(
        """
        SELECT id, user_id
        FROM gamesession
        WHERE user_id = %s
        ORDER BY played_at DESC
        LIMIT 1
        """,
        (current_user_id,)
    )
    result = cursor.fetchone()
    id, user_id = result

    game_session = GameSessionResponse(
        id=id,
        user_id=user_id,
        score=data.score,
        duration=data.duration,
        moves=data.moves,
        played_at=data.played_at
    )
    return game_session

@game_session_router.get(
    "",
    response_model=List[GameSessionResponse],
    summary="Получить список игровых сессий"
)
def list_game_sessions(
    slice: int=5,
    page: int=1,
    conn=Depends(get_db_connection),
    current_user_id=Depends(get_current_user_id)
) -> List[GameSessionResponse]:
    cursor = conn.cursor()
    slice = max(1, min(slice, 20))  # slice between 1 and 20
    page = max(0, page - 1) # page at least 0
    cursor.execute(
        """
        SELECT id, user_id, score, duration, moves, played_at
        FROM gamesession
        ORDER BY played_at DESC
        OFFSET %s
        LIMIT %s
        """,
        (slice * page, slice)
    )

    results = cursor.fetchall()
    dtos = [GameSessionResponse(
        id=r[0],
        user_id=r[1],
        score=r[2],
        duration=r[3],
        moves=r[4],
        played_at=r[5]
    ) for r in results]
    return dtos

@game_session_router.get(
    "/top5",
    response_model=List[GameSessionTopResponse],
    summary="Получить текущий топ 5 игр"
)
def get_top_5_scores(
    conn=Depends(get_db_connection),
    current_user_id=Depends(get_current_user_id)
) -> List[GameSessionResponse]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT u.username, gs.score
        FROM gamesession gs
        JOIN \"user\" u
        ON u.id = gs.user_id
        ORDER BY score DESC
        LIMIT 5
        """
    )
    results = cursor.fetchall()
    if len(results) < 5:
        for _ in range(5 - len(results)):
            results.append((None, None))
    print(results)
    dtos = [GameSessionTopResponse(
        username=r[0],
        score=r[1]
    ) for r in results]
    return dtos

@game_session_router.get(
    "/{id}",
    response_model=GameSessionResponse,
    summary="Получить информацию об игровой сессии с данным id"
)
def get_game_session_by_id(
    id: int,
    conn=Depends(get_db_connection),
    current_user_id=Depends(get_current_user_id)
) -> GameSessionResponse:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, user_id, score, duration, moves, played_at
        FROM gamesession
        WHERE id = %s
        """,
        (id,)
    )

    result = cursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Игровая сессия не найдена"
        )
    id, user_id, score, duration, moves, played_at = result
    gamesession = GameSessionResponse(
        id=id,
        user_id=user_id,
        score=score,
        duration=duration,
        moves=moves,
        played_at=played_at
    )
    return gamesession
