from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_session
from ..services.comicService import getComicById, getComicOfAuthor, searchComic, createNewComic, updateComic
from ..schemas.comic import CreateComicRequest, UpdateComicRequest
from ..core.dependencies import get_current_user, oauth2_scheme
from ..models.usersModel import User
from app.core.dependencies import oauth2_scheme

router = APIRouter(
  prefix="/comic",
  tags=["comic"],
  dependencies=[Depends(oauth2_scheme)]
  # responses={404: {"description": "Not found"}},
)

@router.get('/')
async def getComicDataById(
    title: str | None = None,
    page: int = Query(1, ge=1),
    session: AsyncSession = Depends(get_session)
  ):
  return await searchComic(title, page, session)


@router.post('/create') 
async def createComic( 
    body: CreateComicRequest, 
    current_user: User = Depends(get_current_user), 
    session: AsyncSession = Depends(get_session) 
  ): 
  return await createNewComic(body, current_user, session)


@router.get('/author/{author_id}')
async def getComicListByAuthorId(
    author_id: int,
    page: int = Query(1, ge=1),
    session: AsyncSession = Depends(get_session)
  ):
  return await getComicOfAuthor(author_id, page, session)


@router.put('/update/{comic_id}')
async def updateComicData(
    comic_id: int,
    body: UpdateComicRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
  ):
    return await updateComic(comic_id, body, current_user, session)


@router.get('/{comic_id}')
async def getComicDataById(comic_id: int, session: AsyncSession = Depends(get_session)):
  return await getComicById(comic_id, session)