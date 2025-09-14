from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.comic import CreateComicRequest, UpdateComicRequest
from ..models.usersModel import User
from ..models.comicModel import Comic
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import update


async def banComic(comic_id: int, is_banned: bool, session: AsyncSession):
    try:
        stmt = update(Comic).where(Comic.id == comic_id).values(is_banned=is_banned)
        await session.execute(stmt)
        await session.commit()
        return {"message": "Comic ban status updated successfully"}
    except SQLAlchemyError as e:
        await session.rollback()
        return {"error": str(e)}


async def updateComic(
    comic_id: int, body: UpdateComicRequest, current_user: User, session: AsyncSession
):
    try:
        result = await session.execute(
            select(Comic).where(
                Comic.id == comic_id, Comic.author_id == current_user.id
            )
        )
        comic = result.scalars().one()

        comic.title = body.title if body.title is not None else comic.title
        comic.description = (
            body.description if body.description is not None else comic.description
        )
        comic.cover_url = (
            body.cover_url if body.cover_url is not None else comic.cover_url
        )
        comic.is_published = (
            body.is_published if body.is_published is not None else comic.is_published
        )
        comic.is_premium = (
            body.is_premium if body.is_premium is not None else comic.is_premium
        )
        comic.slug = body.slug if body.slug is not None else comic.slug

        await session.commit()
        await session.refresh(comic)
        return comic
    except NoResultFound:
        return {"error": "Comic not found"}
    except SQLAlchemyError as e:
        await session.rollback()
        return {"error": str(e)}


async def deleteComic(comic_id: int, current_user: User, session: AsyncSession):
    try:
        result = await session.execute(
            select(Comic).where(
                Comic.id == comic_id, Comic.author_id == current_user.id
            )
        )
        comic = result.scalars().one()

        # Deleting related data from other tables
        await session.execute(
            text("DELETE FROM chapters WHERE comic_id = :comic_id"),
            {"comic_id": comic_id},
        )
        await session.execute(
            text("DELETE FROM comic_categories WHERE comic_id = :comic_id"),
            {"comic_id": comic_id},
        )
        await session.execute(
            text("DELETE FROM read_histories WHERE comic_id = :comic_id"),
            {"comic_id": comic_id},
        )

        await session.delete(comic)
        await session.commit()
        return {"message": "Comic and related data deleted successfully"}
    except NoResultFound:
        return {"error": "Comic not found or not authorized to delete"}
    except SQLAlchemyError as e:
        await session.rollback()
        return {"error": str(e)}


async def getComicById(comic_id: int, session: AsyncSession):
    sql = text(
        """
      SELECT c.*, u.username AS author_name, u.email AS author_email, categories
      FROM comics c
      INNER JOIN users u ON c.author_id = u.id
      LEFT JOIN (
      	SELECT ca.comic_id, ARRAY_AGG(cc.name) AS categories
      	FROM comic_categories ca
      	INNER JOIN categories cc ON cc.id = ca.category_id
      	WHERE ca.comic_id = :comic_id
      	GROUP BY ca.comic_id
      ) l on l.comic_id = c.id
      WHERE c.id = :comic_id
    """
    )
    result = await session.execute(sql, {"comic_id": comic_id})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]


async def getComicOfAuthor(author_id: int, page: int, session: AsyncSession):
    sql = text(
        """
      SELECT c.*, u.username AS author_name, u.email AS author_email, categories
      FROM comics c
      INNER JOIN users u ON c.author_id = u.id
      LEFT JOIN (
      	SELECT ca.comic_id, ARRAY_AGG(cc.name) AS categories
      	FROM comic_categories ca
      	INNER JOIN categories cc ON cc.id = ca.category_id
      	GROUP BY ca.comic_id
      ) l on l.comic_id = c.id
      WHERE u.id = :author_id
      ORDER BY c.title
      OFFSET 20 * (:page - 1) LIMIT 20
    """
    )
    result = await session.execute(sql, {"author_id": author_id, "page": page})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]


async def searchComic(title: str | None, page: int, session: AsyncSession):
    titleCondition = "WHERE c.title ILIKE :title" if title else ""
    sqlQuery = f"""SELECT c.*, u.username AS author_name, u.email AS author_email, categories
    FROM comics c
    INNER JOIN users u ON c.author_id = u.id
    LEFT JOIN (
      SELECT ca.comic_id, ARRAY_AGG(cc.name) AS categories
      FROM comic_categories ca
      INNER JOIN categories cc ON cc.id = ca.category_id
      GROUP BY ca.comic_id
    ) l on l.comic_id = c.id
    {titleCondition}
    ORDER BY c.title
    OFFSET 20 * (:page - 1) LIMIT 20
  """
    sql = text(sqlQuery)

    params = {"title": f"%{title}%", "page": page} if title else {"page": page}

    result = await session.execute(sql, params)
    comics = result.fetchall()
    return [dict(row._mapping) for row in comics]


async def createNewComic(
    body: CreateComicRequest, current_user: User, session: AsyncSession
):
    try:
        new_comic = Comic(
            title=body.title,
            description=body.description,
            author_id=current_user.id,
        )
        session.add(new_comic)
        await session.commit()
        await session.refresh(new_comic)
        return new_comic
    except SQLAlchemyError as e:
        await session.rollback()
        return {"error": str(e)}
