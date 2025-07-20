from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.categoryService import listAllCategories

router = APIRouter(
  prefix="/category",
  tags=["category"],
  # dependencies=[Depends(get_token_header)],
  # responses={404: {"description": "Not found"}},
)

@router.get('/')
async def listCategories(page: int = Query(1, ge=1), session: AsyncSession = Depends(get_session)):
  return await listAllCategories(page, session)