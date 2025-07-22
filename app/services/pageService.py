from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def getPagesOfOneChapter(chapter_id: int, session: AsyncSession):
  sql = text(
    """
      SELECT p.*
      FROM pages p
      WHERE p.chapter_id = :chapter_id
      ORDER BY p.page_index
    """
  )
  result = await session.execute(sql, {"chapter_id": chapter_id})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]

async def getOnePage(page_id: int, session: AsyncSession):
  sql = text(
    """
      SELECT p.*
      FROM pages p
      WHERE p.id = :page_id
    """
  )
  result = await session.execute(sql, {"page_id": page_id})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]
