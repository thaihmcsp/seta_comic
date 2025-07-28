from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from sqlalchemy.future import select

from app.models.userSessionModel import UserSession
from app.models.usersModel import User
from app.services.authService import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme),session: AsyncSession = Depends(get_session),) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))
    session_id = payload.get("sid")
    if not session_id or not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    result = await session.execute(
        select(UserSession).where(UserSession.id == session_id)
    )
    session_obj = result.scalar_one_or_none()
    if not session_obj or not session_obj.is_active:
        raise HTTPException(status_code=401, detail="Session expired or revoked")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user