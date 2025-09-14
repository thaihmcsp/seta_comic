from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.comicService import (
    getComicById,
    getComicOfAuthor,
    searchComic,
    createNewComic,
    updateComic,
    deleteComic,
    banComic
)
from ..schemas.comic import CreateComicRequest, UpdateComicRequest
from ..core.dependencies import get_current_user, oauth2_scheme
from ..models.usersModel import User
from app.core.dependencies import oauth2_scheme
from app.schemas.comic import BanComicRequest


router = APIRouter(
    prefix="/comic",
    tags=["comic"],
    dependencies=[Depends(oauth2_scheme)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/")
async def getComicDataById(
    title: str | None = None,
    page: int = Query(1, ge=1),
    session: AsyncSession = Depends(get_session),
):
    return await searchComic(title, page, session)


@router.post("/create")
async def createComic(
    body: CreateComicRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        return {"error": "Unauthorized: Guest role cannot create comics"}
    return await createNewComic(body, current_user, session)


@router.get("/author/{author_id}")
async def getComicListByAuthorId(
    author_id: int,
    page: int = Query(1, ge=1),
    session: AsyncSession = Depends(get_session),
):
    return await getComicOfAuthor(author_id, page, session)


@router.put("/update/{comic_id}")
async def updateComicData(
    comic_id: int,
    body: UpdateComicRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        return {"error": "Unauthorized: Guest role cannot update comics"}
    return await updateComic(comic_id, body, current_user, session)


@router.delete("/delete/{comic_id}")
async def deleteComicData(
    comic_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        return {"error": "Unauthorized: Guest role cannot delete comics"}
    return await deleteComic(comic_id, current_user, session)


from fastapi import Body

@router.put('/ban/{comic_id}')
async def banComicData(
    comic_id: int,
    body: BanComicRequest = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Check if user has admin role
    if 'admin' not in current_user.role:
        return {"error": "Unauthorized: Admin role required"}
    return await banComic(comic_id, body.is_banned, session)


@router.get("/{comic_id}")
async def getComicDataById(comic_id: int, session: AsyncSession = Depends(get_session)):
    return await getComicById(comic_id, session)
