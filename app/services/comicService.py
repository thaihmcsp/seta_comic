from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def getComicById (comic_id: int, session: AsyncSession):
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

async def getComicOfAuthor (author_id: int, page: int, session: AsyncSession):
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

async def searchComic (title: str | None, page: int, session: AsyncSession):
  titleCondition = "WHERE c.title ILIKE :title" if title else ""
  sqlQuery = f'''SELECT c.*, u.username AS author_name, u.email AS author_email, categories
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
  '''
  sql = text(sqlQuery)

  params = {
    "title": f"%{title}%",
    "page": page
  } if title else {
    "page": page
  }

  result = await session.execute(sql, params)
  comics = result.fetchall()
  return [dict(row._mapping) for row in comics]
