from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.chapterService import getChaptersOfComic, getOneChapterData, createChapters, updateChapters, deleteChapter
from ..schemas.chapter import ChaptersCreateRequest, ChaptersUpdateRequest
from ..core.dependencies import get_current_user
from ..models.usersModel import User

router = APIRouter(
  prefix="/chapter",
  tags=["chapter"],
  dependencies=[Depends(get_current_user)],
  # responses={404: {"description": "Not found"}},
)

@router.post('/create')
async def createChaptersAPI(
    body: ChaptersCreateRequest = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        return {"error": "Unauthorized: Guest role cannot create chapters"}
    return await createChapters(body.chapters, current_user, session)

@router.put('/update')
async def updateChaptersAPI(
    body: ChaptersUpdateRequest = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        return {"error": "Unauthorized: Guest role cannot update chapters"}
    return await updateChapters(body.chapters, current_user, session)

@router.delete('/delete/{chapter_id}')
async def deleteChapterAPI(
    chapter_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        return {"error": "Unauthorized: Guest role cannot delete chapters"}
    return await deleteChapter(chapter_id, current_user, session)


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