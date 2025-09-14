from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from fastapi import UploadFile, File, Form


class ActionEnum(str, Enum):
    add = "add"
    update = "update"
    remove = "remove"


class PageUpdateRequest(BaseModel):
    page_index: int
    page_id: int


class BatchEditPagesRequest(BaseModel):
    comic_id: int = Field(..., description="ID of the comic")
    chapter_id: int = Field(..., description="ID of the chapter")
    update: Optional[List[PageUpdateRequest]] = None
    remove: Optional[List[int]] = None  # List of page IDs


class BatchAddPagesRequest(BaseModel):
    files: List[UploadFile] = File(..., description="List of image file Objects")
    page_indexes: List[int] = Form(..., description="List of page indexes")
    comic_id: int = Form(..., description="ID of the comic")
    chapter_id: int = Form(..., description="ID of the chapter")
