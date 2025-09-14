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


async def addCategories(categories: list, session: AsyncSession):
    new_categories = []
    for category in categories:
        sql = text(
            """
      INSERT INTO categories (name, slug)
      VALUES (:name, :slug)
      RETURNING *
      """
        )
        result = await session.execute(
            sql, {"name": category.name, "slug": category.slug}
        )
        new_category = result.fetchone()
        await session.commit()
        new_categories.append(dict(new_category._mapping))
    return new_categories


async def updateCategories(categories: list, session: AsyncSession):
    updated_categories = []
    sql = text(
        """
    UPDATE categories
      SET name = COALESCE(:name, name), slug = COALESCE(:slug, slug)
    WHERE id = :category_id
    RETURNING *
    """
    )
    try:
        for category in categories:
            result = await session.execute(
                sql,
                {
                    "name": category.name,
                    "slug": category.slug,
                    "category_id": category.category_id,
                },
            )
            updated_category = result.fetchone()
            updated_categories.append(dict(updated_category._mapping))
            await session.commit()
        return updated_categories
    except Exception as e:
        await session.rollback()
        raise e


async def deleteCategory(category_id: int, session: AsyncSession):
    # Delete related comic_categories
    await session.execute(
        text("DELETE FROM comic_categories WHERE category_id = :category_id"),
        {"category_id": category_id},
    )
    # Delete category
    await session.execute(
        text("DELETE FROM categories WHERE id = :category_id"),
        {"category_id": category_id},
    )
    await session.commit()
    return {"message": "Category and related comic_categories deleted successfully"}
