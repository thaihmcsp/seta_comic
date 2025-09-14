from pydantic import BaseModel


class CategoryCreateRequest(BaseModel):
    name: str
    slug: str


class CategoryUpdateRequest(BaseModel):
    category_id: int
    name: str
    slug: str
