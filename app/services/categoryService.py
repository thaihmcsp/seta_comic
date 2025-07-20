from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def listAllCategories (page: int, session: AsyncSession):
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
