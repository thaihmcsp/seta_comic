from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.comicService import getComicById, getComicOfAuthor

router = APIRouter(
  prefix="/comic",
  tags=["comic"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

@router.get('/{comic_id}')
async def getComicDataById(comic_id: int, session: AsyncSession = Depends(get_session)):
  return await getComicById(comic_id, session)

@router.get('/author/{author_id}')
async def getComicListByAuthorId(
    author_id: int,
    page: int = Query(1, ge=1),
    session: AsyncSession = Depends(get_session)
  ):
    return await getComicOfAuthor(author_id, page, session)