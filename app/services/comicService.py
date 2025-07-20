from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def getComicById (comic_id: int, session: AsyncSession):
  sql = text(
    """
      SELECT c.*, u.username AS author_name, u.email AS author_email
      FROM comics c
      INNER JOIN users u ON c.author_id = u.id
      WHERE c.id = :comic_id
    """
  )
  result = await session.execute(sql, {"comic_id": comic_id})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]
