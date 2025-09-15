from typing import List
from pydantic import BaseModel


class ComicCategoryAddRequest(BaseModel):
    comic_id: int
    categories: List[int]


class ComicCategoryUpdateRequest(BaseModel):
    comic_id: int
    categories: List[int]


class CategoryInfo(BaseModel):
    id: int
    name: str
    slug: str


class ComicInfo(BaseModel):
    id: int
    title: str
    description: str | None
    cover_url: str | None
    is_published: bool
    is_banned: bool
    is_premium: bool
    slug: str
    author_id: int
