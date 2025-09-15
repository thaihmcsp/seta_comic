from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from fastapi import APIRouter, Depends, Query, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.categoryService import listAllCategories, getComicForCategory, addCategories, updateCategories, deleteCategory
from ..core.dependencies import get_current_user
from ..models.usersModel import User
from typing import List
from ..schemas.category import CategoryCreateRequest, CategoryUpdateRequest

router = APIRouter(
  prefix="/category",
  tags=["category"],
  # dependencies=[Depends(get_current_user)],
  # responses={404: {"description": "Not found"}},
)


@router.post('/add')
async def addCategoriesAPI(
  body: List[CategoryCreateRequest] = Body(...),
  current_user: User = Depends(get_current_user),
  session: AsyncSession = Depends(get_session)
):
  if 'admin' not in current_user.role:
    raise HTTPException(status_code=403, detail="Unauthorized: Admin role required")
  return await addCategories(body, session)


@router.put('/update')
async def updateCategoriesAPI(
  body: List[CategoryUpdateRequest] = Body(...),
  current_user: User = Depends(get_current_user),
  session: AsyncSession = Depends(get_session)
):
  if 'admin' not in current_user.role:
    raise HTTPException(status_code=403, detail="Unauthorized: Admin role required")
  return await updateCategories(body, session)


@router.delete('/{category_id}')
async def deleteCategoryAPI(
  category_id: int,
  current_user: User = Depends(get_current_user),
  session: AsyncSession = Depends(get_session)
):
  if 'admin' not in current_user.role:
    raise HTTPException(status_code=403, detail="Unauthorized: Admin role required")
  return await deleteCategory(category_id, session)


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