import os
import boto3
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, update
from app.services.authService import verify_password, hash_password
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)
bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

async def listUser(session: AsyncSession):
    sql = text("SELECT * FROM users")
    result = await session.execute(sql)
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]


async def getUserByUserId(user_id: int, session: AsyncSession):
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


async def searchAuthorByText(page: int, name: str | None, session: AsyncSession):
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

    params = {"name": f"%{name}%", "page": page} if name else {"page": page}

    result = await session.execute(sql, params)
    authors = result.fetchall()
    return [dict(row._mapping) for row in authors]


async def changePassword(
    user_id: int, old_password: str, new_password: str, session: AsyncSession
):
    try:
        sql = text("SELECT password_hash FROM users WHERE id = :user_id")
        result = await session.execute(sql, {"user_id": user_id})
        row = result.fetchone()
        if not row:
            raise NoResultFound("User not found")

        hashed_password = row[0]

        if not verify_password(old_password, hashed_password):
            raise ValueError("Old password is incorrect")

        new_hashed_password = hash_password(new_password)

        update_sql = text(
            "UPDATE users SET password_hash = :password WHERE id = :user_id"
        )
        await session.execute(
            update_sql, {"password": new_hashed_password, "user_id": user_id}
        )

        # Set all sessions for this user to inactive
        update_session_sql = text(
            "UPDATE user_sessions SET is_active = false WHERE user_id = :user_id"
        )
        await session.execute(update_session_sql, {"user_id": user_id})

        await session.commit()

        return {"message": "Password changed successfully"}
    except SQLAlchemyError as e:
        await session.rollback()
        return {"error": str(e)}


async def updateUser(
    user_id: int, username: str | None, email: str | None, avatar, session: AsyncSession
):
    try:
        update_data = {}
        if username:
            update_data["username"] = username
        if email:
            update_data["email"] = email

        if avatar:
            # Upload avatar to S3
            file_name = f"avatars/user_{user_id}.jpg"
            url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
            s3_client.upload_fileobj(avatar.file, bucket_name, file_name)
            update_data["avatar_url"] = url

        if not update_data:
            raise ValueError("No data provided for update")

        update_sql = text(
            """
              UPDATE users
              SET username = COALESCE(:username, username),
                  email = COALESCE(:email, email),
                  avatar_url = COALESCE(:avatar_url, avatar_url)
              WHERE id = :user_id
              RETURNING *
            """
        )

        result = await session.execute(update_sql, {**update_data, "user_id": user_id})
        updated_user = result.fetchone()
        await session.commit()

        if updated_user:
            return dict(updated_user._mapping)
        else:
            raise NoResultFound("User not found")
    except Exception as e:
        await session.rollback()
        return {"error": str(e)}
