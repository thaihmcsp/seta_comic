from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def listAllCategories(page: int, session: AsyncSession):
  sql = text(
      """
    SELECT c.*
    FROM categories c
    ORDER BY c.name
    OFFSET 20 * (:page - 1) LIMIT 20
  """
  )
  result = await session.execute(sql, {"page": page})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]


async def getComicForCategory(category_id: int, page: int, session: AsyncSession):
  sql = text(
      """
    SELECT ca.*, cc.comic_id, c.title, c.author_id, u.username AS author_name
    FROM categories ca
    LEFT JOIN comic_categories cc ON cc.category_id = ca.id
    LEFT JOIN comics c ON c.id = cc.comic_id
    LEFT JOIN users u ON u.id = c.author_id
    WHERE ca.id = :category_id
    ORDER BY c.title
    OFFSET 20 * (:page - 1) LIMIT 20
  """
  )
  result = await session.execute(sql, {"page": page, "category_id": category_id})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]
