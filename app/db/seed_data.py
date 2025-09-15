import asyncio
import random
from datetime import datetime, timedelta, date
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.usersModel import User, UserRole, UserStatus
from app.models.comicModel import Comic
from app.models.chapterModel import Chapter
from app.models.pageModel import Pages
from app.models.categoryModel import Category, Comic_Category
from app.models.commentModel import Comment, Like
from app.models.favoriteModel import Favorite
from app.models.readHistoryModel import History
from app.models.userSessionModel import UserSession

from app.db.session import async_session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_data():
    """Seed the database with 10 records for each table."""
    async with async_session() as session:
        # Seed users
        users = await seed_users(session)
        
        # Seed categories
        categories = await seed_categories(session)
        
        # Seed comics
        comics = await seed_comics(session, users)
        
        # Seed comic_categories
        await seed_comic_categories(session, comics, categories)
        
        # Seed chapters
        chapters = await seed_chapters(session, comics, users)
        
        # Seed pages
        await seed_pages(session, comics, chapters)
        
        # Seed comments
        comments = await seed_comments(session, comics, chapters, users)
        
        # Seed likes
        await seed_likes(session, comments, users)
        
        # Seed favorites
        await seed_favorites(session, comics, users)
        
        # Seed read histories
        await seed_read_histories(session, comics, chapters, users)
        
        # Seed user sessions
        await seed_user_sessions(session, users)
        
        await session.commit()
        
    print("Database seeded successfully!")

async def seed_users(session: AsyncSession):
    """Seed 10 users."""
    users = []
    roles = list(UserRole)
    statuses = list(UserStatus)
    
    for i in range(1, 11):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password_hash=pwd_context.hash(f"password{i}"),
            avatar_url=f"https://example.com/avatars/user{i}.jpg",
            is_premium=i % 3 == 0,  # Every 3rd user is premium
            role=roles[i % len(roles)],
            user_status=statuses[i % len(statuses)]
        )
        session.add(user)
        users.append(user)
    
    await session.flush()
    return users

async def seed_categories(session: AsyncSession):
    """Seed 10 categories."""
    category_names = [
        "Action", "Adventure", "Comedy", "Drama", "Fantasy", 
        "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller"
    ]
    
    categories = []
    for name in category_names:
        category = Category(
            name=name,
            slug=name.lower().replace(" ", "-")
        )
        session.add(category)
        categories.append(category)
    
    await session.flush()
    return categories

async def seed_comics(session: AsyncSession, users):
    """Seed 10 comics."""
    comic_titles = [
        "The Amazing Adventure", "Dark Knight's Journey", "Magical World", 
        "Space Explorers", "Zombie Apocalypse", "Love in Paris", 
        "Detective Stories", "Fantasy Kingdom", "Superhero Chronicles", 
        "Mysterious Island"
    ]
    
    comics = []
    for i, title in enumerate(comic_titles):
        comic = Comic(
            title=title,
            description=f"Description for {title}. This is an exciting comic that readers will love!",
            cover_url=f"https://example.com/covers/{i+1}.jpg",
            is_published=True,
            is_banned=False,
            is_premium=i % 3 == 0,  # Every 3rd comic is premium
            slug=title.lower().replace(" ", "-").replace("'", ""),
            author_id=users[i % len(users)].id
        )
        session.add(comic)
        comics.append(comic)
    
    await session.flush()
    return comics

async def seed_comic_categories(session: AsyncSession, comics, categories):
    """Seed comic_categories junction table."""
    for comic in comics:
        # Assign 2-3 random categories to each comic
        num_categories = random.randint(2, 3)
        selected_categories = random.sample(categories, num_categories)
        
        for category in selected_categories:
            comic_category = Comic_Category(
                comic_id=comic.id,
                category_id=category.id
            )
            session.add(comic_category)
    
    await session.flush()

async def seed_chapters(session: AsyncSession, comics, users):
    """Seed 10 chapters for each comic."""
    chapters = []
    
    for comic in comics:
        for i in range(1, 11):
            release_date = date.today() - timedelta(days=i*3)
            chapter = Chapter(
                title=f"Chapter {i}: The Adventure Continues",
                chapter_number=i,
                release_date=release_date,
                comic_id=comic.id,
                author_id=comic.author_id if i % 2 == 0 else random.choice(users).id
            )
            session.add(chapter)
            chapters.append(chapter)
    
    await session.flush()
    return chapters

async def seed_pages(session: AsyncSession, comics, chapters):
    """Seed 10 pages for each chapter."""
    for chapter in chapters:
        for i in range(1, 11):
            page = Pages(
                image_url=f"https://example.com/comics/{chapter.comic_id}/chapters/{chapter.id}/pages/{i}.jpg",
                page_index=i,
                comic_id=chapter.comic_id,
                chapter_id=chapter.id
            )
            session.add(page)
    
    await session.flush()

async def seed_comments(session: AsyncSession, comics, chapters, users):
    """Seed 10 comments."""
    comments = []
    comment_contents = [
        "Great chapter!", "I love this comic!", "Can't wait for the next chapter!",
        "The artwork is amazing!", "This story is getting interesting!",
        "I didn't expect that twist!", "The characters are so well developed!",
        "This is my favorite comic!", "The plot is amazing!", "Awesome work!"
    ]
    
    for i, content in enumerate(comment_contents):
        # Alternate between commenting on comics and chapters
        if i % 2 == 0:
            comic = random.choice(comics)
            comment = Comment(
                content=content,
                comic_id=comic.id,
                chapter_id=None,
                user_id=random.choice(users).id
            )
        else:
            chapter = random.choice(chapters)
            comment = Comment(
                content=content,
                comic_id=None,
                chapter_id=chapter.id,
                user_id=random.choice(users).id
            )
        
        session.add(comment)
        comments.append(comment)
    
    await session.flush()
    return comments

async def seed_likes(session: AsyncSession, comments, users):
    """Seed likes for comments."""
    for comment in comments:
        # Add 1-5 likes for each comment
        num_likes = random.randint(1, 5)
        liking_users = random.sample(users, min(num_likes, len(users)))
        
        for user in liking_users:
            like = Like(
                comment_id=comment.id,
                user_id=user.id
            )
            session.add(like)
    
    await session.flush()

async def seed_favorites(session: AsyncSession, comics, users):
    """Seed favorites."""
    for user in users:
        # Each user favorites 1-3 comics
        num_favorites = random.randint(1, 3)
        favorited_comics = random.sample(comics, min(num_favorites, len(comics)))
        
        for comic in favorited_comics:
            favorite = Favorite(
                comic_id=comic.id,
                user_id=user.id
            )
            session.add(favorite)
    
    await session.flush()

async def seed_read_histories(session: AsyncSession, comics, chapters, users):
    """Seed read histories."""
    for user in users:
        # Each user has read 1-5 chapters
        num_reads = random.randint(1, 5)
        read_chapters = random.sample(chapters, min(num_reads, len(chapters)))
        
        for chapter in read_chapters:
            history = History(
                comic_id=chapter.comic_id,
                chapter_id=chapter.id,
                user_id=user.id
            )
            session.add(history)
    
    await session.flush()

async def seed_user_sessions(session: AsyncSession, users):
    """Seed user sessions."""
    for user in users:
        # Each user has 1-2 sessions
        num_sessions = random.randint(1, 2)
        
        for _ in range(num_sessions):
            is_active = random.choice([True, False])
            user_session = UserSession(
                id=str(uuid.uuid4()),
                user_id=user.id,
                is_active=is_active
            )
            session.add(user_session)
    
    await session.flush()

if __name__ == "__main__":
    asyncio.run(seed_data())