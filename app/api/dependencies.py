from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.auth import decode_token

security = HTTPBearer()

def get_current_user_id(token: HTTPAuthorizationCredentials = Depends(security)) -> int:
    payload = decode_token(token.credentials)
    user_id = payload.get("id")
    if not payload or not user_id:
        raise HTTPException(status_code=403, detail="Неверные учетные данные")
    return int(user_id)
