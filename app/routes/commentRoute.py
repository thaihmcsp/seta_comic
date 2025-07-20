from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.commentService import getCommentOfComic

router = APIRouter(
  prefix="/comment",
  tags=["comment"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)


@router.get("/comic/{comic_id}")
async def listComment(
  comic_id: int,
  page: int = Query(1, ge=1),
  session: AsyncSession = Depends(get_session),
):
  return await getCommentOfComic(comic_id, page, session)
