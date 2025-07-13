from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Date
from .base import Base

class Pages(Base):
  __tablename__ = 'pages'

  id = Column(Integer, primary_key=True, index=True)
  image_url = Column(String, index=True)
  page_index = Column(Integer, nullable=False)

  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  comic_id = Column(Integer, ForeignKey('comics.id'))
  chapter_id = Column(Integer, ForeignKey('chapters.id'))
