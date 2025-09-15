from fastapi import APIRouter, Depends, Query, HTTPException, Body
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
from ..schemas.comic_category import ComicCategoryAddRequest, ComicCategoryUpdateRequest
from ..core.dependencies import get_current_user, oauth2_scheme
from ..models.usersModel import User
from app.core.dependencies import oauth2_scheme
from app.schemas.comic import BanComicRequest
from sqlalchemy import text


router = APIRouter(
    prefix="/comic",
    tags=["comic"],
    # dependencies=[Depends(oauth2_scheme)],
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
        raise HTTPException(status_code=403, detail="Unauthorized: Guest role cannot create comics")
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
        raise HTTPException(status_code=403, detail="Unauthorized: Guest role cannot update comics")
    return await updateComic(comic_id, body, current_user, session)


@router.delete("/delete/{comic_id}")
async def deleteComicData(
    comic_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if 'guest' in current_user.role:
        raise HTTPException(status_code=403, detail="Unauthorized: Guest role cannot delete comics")
    return await deleteComic(comic_id, current_user, session)


@router.post("/add-categories")
async def addComicCategories(
    body: ComicCategoryAddRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Validate user is author of comic
    result = await session.execute(text("SELECT author_id FROM comics WHERE id = :comic_id"), {"comic_id": body.comic_id})
    author_id = result.scalar()
    if author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized: User is not the author of the comic")

    # Insert categories
    for category_id in body.categories:
        await session.execute(text("INSERT INTO comic_categories (comic_id, category_id) VALUES (:comic_id, :category_id) ON CONFLICT DO NOTHING"), {"comic_id": body.comic_id, "category_id": category_id})
    await session.commit()

    # Fetch comic info and categories
    comic_result = await session.execute(text("SELECT * FROM comics WHERE id = :comic_id"), {"comic_id": body.comic_id})
    comic_row = comic_result.first()
    if not comic_row:
        raise HTTPException(status_code=404, detail="Comic not found")

    categories_result = await session.execute(text("SELECT id, name, slug FROM categories WHERE id IN (SELECT category_id FROM comic_categories WHERE comic_id = :comic_id)"), {"comic_id": body.comic_id})
    categories_rows = categories_result.fetchall()
    comic_dict = dict(comic_row._mapping)
    categories_list = [dict(row._mapping) for row in categories_rows]

    return {"comic": comic_dict, "categories": categories_list}


@router.put("/update-categories")
async def updateComicCategories(
    body: ComicCategoryUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Validate user is author of comic
    result = await session.execute(text("SELECT author_id FROM comics WHERE id = :comic_id"), {"comic_id": body.comic_id})
    author_id = result.scalar()
    if author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized: User is not the author of the comic")

    # Delete old categories
    await session.execute(text("DELETE FROM comic_categories WHERE comic_id = :comic_id"), {"comic_id": body.comic_id})

    # Insert new categories
    for category_id in body.categories:
        await session.execute(text("INSERT INTO comic_categories (comic_id, category_id) VALUES (:comic_id, :category_id) ON CONFLICT DO NOTHING"), {"comic_id": body.comic_id, "category_id": category_id})

    await session.commit()
    # Fetch comic info and categories
    comic_result = await session.execute(text("SELECT * FROM comics WHERE id = :comic_id"), {"comic_id": body.comic_id})
    comic_row = comic_result.first()
    if not comic_row:
        raise HTTPException(status_code=404, detail="Comic not found")

    categories_result = await session.execute(text("SELECT id, name, slug FROM categories WHERE id IN (SELECT category_id FROM comic_categories WHERE comic_id = :comic_id)"), {"comic_id": body.comic_id})
    categories_rows = categories_result.fetchall()

    comic_dict = dict(comic_row._mapping)
    categories_list = [dict(row._mapping) for row in categories_rows]

    return {"comic": comic_dict, "categories": categories_list}


@router.put('/ban/{comic_id}')
async def banComicData(
    comic_id: int,
    body: BanComicRequest = Body(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Check if user has admin role
    if 'admin' not in current_user.role:
        raise HTTPException(status_code=403, detail="Unauthorized: Admin role required")
    return await banComic(comic_id, body.is_banned, session)


@router.get("/{comic_id}")
async def getComicDataById(comic_id: int, session: AsyncSession = Depends(get_session)):
    return await getComicById(comic_id, session)
