from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def listUser(session: AsyncSession):
  sql = text("SELECT * FROM users")
  result = await session.execute(sql)
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]

async def getUserByUserId (user_id: int, session: AsyncSession):
  sql = text("SELECT * FROM users WHERE id = :user_id")
  result = await session.execute(sql, {"user_id": user_id})
  row = result.fetchone()
  return dict(row._mapping) if row else None
