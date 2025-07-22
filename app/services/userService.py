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

async def searchAuthorByText (page: int, name: str | None, session: AsyncSession):
  searchCondition = "WHERE u.username ILIKE :name" if name else ""
  sql_str = f"""
    SELECT u.id, u.username, u.email, u.avatar_url, u.user_status
    FROM (
      SELECT DISTINCT author_id from comics
    ) c
    INNER JOIN users u ON c.author_id = u.id
    {searchCondition}
    ORDER BY u.username
    OFFSET 20 * (:page - 1) LIMIT 20
  """
  sql = text(sql_str)

  params = {
    "name": f"%{name}%",
    "page": page
  } if name else {
    "page": page
  }

  result = await session.execute(sql, params)
  authors = result.fetchall()
  return [dict(row._mapping) for row in authors]
