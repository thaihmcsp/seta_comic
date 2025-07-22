from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def getCommentOfComic (comic_id: int, page: int, session: AsyncSession):
  sql = text(
      """
    SELECT c.*, u.username
    FROM comments c
    INNER JOIN users u ON u.id = c.user_id
    WHERE c.comic_id = :comic_id and c.chapter_id IS NULL
    ORDER BY c.created_at
    OFFSET 20 * (:page - 1) LIMIT 20
  """
  )

  result = await session.execute(sql, {"page": page, "comic_id": comic_id})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]



async def getCommentOfChapter (chapter_id: int, page: int, session: AsyncSession):
  sql = text(
      """
    SELECT c.*, u.username
    FROM comments c
    INNER JOIN users u ON u.id = c.user_id
    WHERE c.chapter_id = :chapter_id
    ORDER BY c.created_at
    OFFSET 20 * (:page - 1) LIMIT 20
  """
  )

  result = await session.execute(sql, {"page": page, "chapter_id": chapter_id})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]
