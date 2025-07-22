from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.userService import listUser, getUserByUserId, searchAuthorByText
from app.db.deps import get_session

router = APIRouter(
  prefix="/user",
  tags=["user"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

# need check auth
@router.get('/me')
async def getMyInfo():
  return {"username": "test", "email": "test@gmail.com"}

# need check role admin
@router.get('/')
async def getlistUser(session: AsyncSession = Depends(get_session)):
  return await listUser(session)

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