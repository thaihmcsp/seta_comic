from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.userService import listUser, getUserByUserId, searchAuthorByText, searchAuthorByText

from ..core.dependencies import get_current_user
from ..models.usersModel import User
from ..schemas.user import UserOut
from app.db.deps import get_session

router = APIRouter(
  prefix="/user",
  tags=["user"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

@router.get('/me')
async def getMyInfo(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)

@router.get('/list')
async def getUserList(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
  if current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Not authorized")
  users = await listUser(session)
  return users

@router.get('/authors')
async def searchAuthors(
    page: int = Query(1, ge=1),
    name: str | None = None,
    session: AsyncSession = Depends(get_session)
  ):
  return await searchAuthorByText(page, name, session)

@router.get('/{user_id}')
async def getUserById(user_id: int, session: AsyncSession = Depends(get_session)):
  return await getUserByUserId(user_id, session)
async def getUserById(user_id: int, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
  if current_user.id != user_id and current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Not authorized")
  user = await getUserByUserId(user_id, session)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return user
