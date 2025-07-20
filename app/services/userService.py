from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def listUser(session: AsyncSession):
  sql = text("SELECT * FROM users")
  result = await session.execute(sql)
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]

async def getUserByUserId (user_id: int, session: AsyncSession):
  sql = text(
    """
      SELECT u.id, u.username, u.email, u.avatar_url, u.user_status, c.title AS comic_title
      FROM users u
      LEFT JOIN comics c ON c.author_id = u.id
      WHERE u.id = :user_id
    """
  )
  result = await session.execute(sql, {"user_id": user_id})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]
