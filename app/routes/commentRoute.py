from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.commentService import getCommentOfComic, getCommentOfChapter

router = APIRouter(
  prefix="/comment",
  tags=["comment"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)


@router.get("/comic/{comic_id}")
async def listComicComment(
  comic_id: int,
  page: int = Query(1, ge=1),
  session: AsyncSession = Depends(get_session),
):
  return await getCommentOfComic(comic_id, page, session)


@router.get("/chapter/{chapter_id}")
async def listChapterComment(
  chapter_id: int,
  page: int = Query(1, ge=1),
  session: AsyncSession = Depends(get_session),
):
  return await getCommentOfChapter(chapter_id, page, session)
