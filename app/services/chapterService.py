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

async def getOneChapterData(chapter_id: int, session: AsyncSession):
  sql = text(
    """
      SELECT c.*
      FROM chapters c
      WHERE c.id = :chapter_id
    """
  )
  result = await session.execute(sql, {"chapter_id": chapter_id})
  rows = result.fetchall()
  return [dict(row._mapping) for row in rows]


async def createChapters(chapters: list, current_user, session: AsyncSession):
  created_chapters = []
  for chapter in chapters:
    # Check if comic author matches current user
    comic_check = await session.execute(text("SELECT author_id FROM comics WHERE id = :comic_id"), {"comic_id": chapter.comic_id})
    if comic_check is None:
      created_chapters.append(dict(chapter, error="Comic not found"))
      continue
    
    comic_author = comic_check.scalar_one_or_none()
    if comic_author != current_user.id:
      created_chapters.append(dict(chapter, error="Unauthorized to create chapter for this comic"))
      continue

    sql = text(
      """
      INSERT INTO chapters (title, chapter_number, comic_id, author_id)
      VALUES (:title, :chapter_number, :comic_id, :author_id)
      RETURNING *
      """
    )
    result = await session.execute(sql, {
      "title": chapter.title,
      "chapter_number": chapter.chapter_number,
      "comic_id": chapter.comic_id,
      "author_id": current_user.id
    })
    created_chapter = result.fetchone()
    await session.commit()
    created_chapters.append(dict(created_chapter._mapping))

  return created_chapters


async def updateChapters(chapters: list, current_user, session: AsyncSession):
  updated_chapters = []
  for chapter in chapters:
    # Check if comic author matches current user
    comic_check = await session.execute(text("SELECT author_id FROM comics WHERE id = :comic_id"), {"comic_id": chapter.comic_id})
    if comic_check is None:
      updated_chapters.append(dict(chapter, error="Comic not found"))
      continue

    comic_author = comic_check.scalar_one_or_none()
    if comic_author != current_user.id:
      updated_chapters.append(dict(chapter, error="Unauthorized to update chapter for this comic"))
      continue

    sql = text(
      """
      UPDATE chapters
      SET title = COALESCE(:title, title),
          chapter_number = COALESCE(:chapter_number, chapter_number)
      WHERE id = :chapter_id
      RETURNING *
      """
    )
    result = await session.execute(sql, {
      "title": chapter.title,
      "chapter_number": chapter.chapter_number,
      "chapter_id": chapter.chapter_id
    })
    updated_chapter = result.fetchone()
    await session.commit()
    updated_chapters.append(dict(updated_chapter._mapping))

  return updated_chapters


async def deleteChapter(chapter_id: int, current_user, session: AsyncSession):
  # Check if comic author matches current user
  comic_check = await session.execute(text("SELECT author_id FROM comics WHERE id = (SELECT comic_id FROM chapters WHERE id = :chapter_id)"), {"chapter_id": chapter_id})
  comic_author = comic_check.scalar_one_or_none()
  if comic_author != current_user.id:
    return {"error": "Unauthorized to delete this chapter"}

  # Delete pages that refer to this chapter
  await session.execute(text("DELETE FROM pages WHERE chapter_id = :chapter_id"), {"chapter_id": chapter_id})

  # Delete the chapter
  await session.execute(text("DELETE FROM chapters WHERE id = :chapter_id"), {"chapter_id": chapter_id})
  await session.commit()

  return {"message": "Chapter and related pages deleted successfully"}

