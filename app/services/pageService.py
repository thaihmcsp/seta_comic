from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import boto3
from botocore.exceptions import NoCredentialsError
import os
from sqlalchemy import select
from ..models.pageModel import Pages
from ..models.comicModel import Comic
from ..models.chapterModel import Chapter
from fastapi import HTTPException

# AWS S3 connection setup
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)
S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")



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


async def upload_image_to_s3(file_content, file_name):
    try:
        url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
         # Upload the file stream
        s3_client.upload_fileobj(file_content.file, S3_BUCKET_NAME, file_name)
        return url
    except NoCredentialsError:
        return None


async def batchAddPages(files, page_indexes, comic_id, chapter_id, current_user, session: AsyncSession):
    # Check author_id of comic and chapter
    comic_res = await session.execute(select(Comic).where(Comic.id == comic_id))
    comic = comic_res.scalars().one_or_none()
    chapter_res = await session.execute(
        select(Chapter).where(Chapter.id == chapter_id)
    )
    chapter = chapter_res.scalars().one_or_none()
    if (
        not comic
        or not chapter
        or comic.author_id != current_user.id
        or chapter.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail="Unauthorized to add pages to this comic"
        )

    # Handle add
    created_pages = []
    if files and page_indexes:
        for idx, file_content in enumerate(files):
            page_index = page_indexes[idx]
            fileExtension = os.path.splitext(file_content.filename)[1]
            if fileExtension.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                continue
            
            # Upload image to S3
            print(86666, "Uploading image to S3...")
            image_url = await upload_image_to_s3(
                file_content,
                f"pages/comic{comic_id}_chap{chapter_id}_page{page_index}",
            )
            if not image_url:
                continue

            print(94444, "Image uploaded to S3:", image_url)    
              
            new_page = Pages(
                image_url=image_url,
                page_index=page_index,
                comic_id=comic_id,
                chapter_id=chapter_id,
            )
            session.add(new_page)
            await session.commit()
            await session.refresh(new_page)
            created_pages.append(new_page)

    return created_pages


async def batchEditPages(body, current_user, session: AsyncSession):
    # Check author_id of comic and chapter
    comic_res = await session.execute(
        select(Comic).where(Comic.id == body.comic_id)
    )
    comic = comic_res.scalars().one_or_none()
    chapter_res = await session.execute(
        select(Chapter).where(Chapter.id == body.chapter_id)
    )
    chapter = chapter_res.scalars().one_or_none()
    if (
        not comic
        or not chapter
        or comic.author_id != current_user.id
        or chapter.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403, detail="Unauthorized to edit pages of this comic"
        )
  
    # Handle remove
    if body.remove:
        for page_id in body.remove:
            # Check author_id of comic and chapter
            page_res = await session.execute(select(Pages).where(Pages.id == page_id))
            page_obj = page_res.scalars().one_or_none()
            if not page_obj:
                raise HTTPException(status_code=404, detail="Page not found")
            if page_obj.chapter_id != body.chapter_id or page_obj.comic_id != body.comic_id:
                raise HTTPException(status_code=403, detail="Unauthorized to delete this page")
            
            # Optionally: Delete image from S3
            image_key = page_obj.image_url.split(f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/")[-1]
            try:
                s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=image_key)
            except NoCredentialsError:
                pass  # Log error if needed but continue to delete DB record
                
            # Delete page
            await session.delete(page_obj)
        await session.commit()
  
    # Handle update
    if body.update:
        for page in body.update:
            # Update page
            update_stmt = text(
                """
                UPDATE pages
                SET page_index = COALESCE(:page_index, page_index)
                WHERE id = :page_id
                RETURNING *
                """
            )
            await session.execute(
                update_stmt,
                {
                    "page_index": page.page_index,
                    "page_id": page.page_id,
                },
            )
        await session.commit()

    return {"message": "Batch edit completed"}
