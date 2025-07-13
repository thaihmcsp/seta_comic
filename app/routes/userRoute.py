from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.userService import listUser, getUserByUserId
from app.db.deps import get_session

router = APIRouter(
  prefix="/user",
  tags=["user"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

@router.get('/me')
async def getMyInfo():
  return {"username": "test", "email": "test@gmail.com"}

@router.get('/')
async def getlistUser(session: AsyncSession = Depends(get_session)):
  return await listUser(session)

@router.get('/{user_id}')
async def getUserById(user_id: int, session: AsyncSession = Depends(get_session)):
  print(23, user_id)
  return await getUserByUserId(user_id, session)