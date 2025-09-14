from typing import Optional

from pydantic import BaseModel, Field

class BanComicRequest(BaseModel):
    is_banned: bool = Field(..., description="Ban status of the comic")

class UpdateComicRequest(BaseModel):
    title: Optional[str] = Field(None, title="Title of the comic")
    description: Optional[str] = Field(None, description="Description of the comic")
    cover_url: Optional[str] = Field(None, description="Cover URL of the comic")
    is_published: Optional[bool] = Field(None, description="Publication status of the comic")
    is_premium: Optional[bool] = Field(None, description="Premium status of the comic")
    slug: Optional[str] = Field(None, description="Slug for the comic")


class CreateComicRequest(BaseModel):
    title: str
    description: Optional[str]
    cover_url: Optional[str]
