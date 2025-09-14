from typing import List, Optional
from pydantic import BaseModel, Field


class ChapterCreateRequest(BaseModel):
    title: str
    chapter_number: int
    comic_id: int


class ChapterUpdateRequest(BaseModel):
    chapter_id: int
    title: Optional[str] = None
    chapter_number: Optional[int] = None
    comic_id: Optional[int] = None


class ChaptersCreateRequest(BaseModel):
    chapters: List[ChapterCreateRequest]


class ChaptersUpdateRequest(BaseModel):
    chapters: List[ChapterUpdateRequest]
