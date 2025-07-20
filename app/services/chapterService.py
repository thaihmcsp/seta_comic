from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def getChaptersOfComic (comic_id: int, page: int, session: AsyncSession):
  sql = text(
    """
      SELECT c.*
      FROM chapters c
      WHERE c.comic_id = :comic_id
      ORDER BY c.chapter_number
      OFFSET 20 * (:page - 1) LIMIT 20
    """
  )
  result = await session.execute(sql, {"comic_id": comic_id, "page": page})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]