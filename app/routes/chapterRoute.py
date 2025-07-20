from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.chapterService import getChaptersOfComic, getOneChapterData

router = APIRouter(
  prefix="/chapter",
  tags=["chapter"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

@router.get("/comic/{comic_id}")
async def getChaptersByComicId(
    comic_id: int,
    page: int = Query(1, ge=1),
    session: AsyncSession = Depends(get_session)
  ):
  return await getChaptersOfComic(comic_id, page, session)

@router.get("/{chapter_id}")
async def getChapterById(
    chapter_id: int,
    session: AsyncSession = Depends(get_session)
  ):
  return await getOneChapterData(chapter_id, session)