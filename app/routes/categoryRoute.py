from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.categoryService import listAllCategories, getComicForCategory

router = APIRouter(
  prefix="/category",
  tags=["category"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)


@router.get("/")
async def listCategories(
  page: int = Query(1, ge=1), session: AsyncSession = Depends(get_session)
):
  return await listAllCategories(page, session)


@router.get("/{category_id}")
async def listCategories(
  category_id: int,
  page: int = Query(1, ge=1),
  session: AsyncSession = Depends(get_session),
):
  return await getComicForCategory(category_id, page, session)
