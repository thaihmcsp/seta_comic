from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.pageService import getPagesOfOneChapter, getOnePage

router = APIRouter(
  prefix="/page",
  tags=["page"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

@router.get("/chapter/:chapter_id")
async def getListPageOfChapter(
    chapter_id: int,
    session: AsyncSession = Depends(get_session)
  ):
  return await getPagesOfOneChapter(chapter_id, session)

@router.get("/:page_id")
async def getPageById(
    page_id: int,
    session: AsyncSession = Depends(get_session)
  ):
  return await getOnePage(page_id, session)
