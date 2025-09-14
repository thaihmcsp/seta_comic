from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.pageService import getPagesOfOneChapter, getOnePage, batchEditPages, batchAddPages
from ..schemas.page import BatchEditPagesRequest, BatchAddPagesRequest
from ..core.dependencies import get_current_user
from ..models.usersModel import User
from fastapi import UploadFile, File, Form
from typing import List

router = APIRouter(
  prefix="/page",
  tags=["page"],
  dependencies=[Depends(get_current_user)],
  # responses={404: {"description": "Not found"}},
)


@router.post('/add')
async def batchAddPagesAPI(
    files: List[UploadFile] = File(..., description="List of image file Objects"),
    page_indexes: List[int] = Form(..., description="List of page indexes"),
    comic_id: int = Form(..., description="ID of the comic"),
    chapter_id: int = Form(..., description="ID of the chapter"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        raise HTTPException(status_code=403, detail="Unauthorized: Guest role cannot edit pages")
    return await batchAddPages(files, page_indexes, comic_id, chapter_id, current_user, session)


@router.put('/batch-edit')
async def batchEditPagesAPI(
    body: BatchEditPagesRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        raise HTTPException(status_code=403, detail="Unauthorized: Guest role cannot edit pages")
    return await batchEditPages(body, current_user, session)


@router.get("/chapter/{chapter_id}")
async def getListPageOfChapter(
    chapter_id: int,
    session: AsyncSession = Depends(get_session)
  ):
  return await getPagesOfOneChapter(chapter_id, session)


@router.get("/{page_id}")
async def getPageById(
    page_id: int,
    session: AsyncSession = Depends(get_session)
  ):
  return await getOnePage(page_id, session)
