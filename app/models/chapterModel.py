from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Date
from .base import Base

class Chapter(Base):
  __tablename__ = 'chapters'

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  chapter_number = Column(Integer, nullable=False)

  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  release_date = Column(Date, nullable=False)

  comic_id = Column(Integer, ForeignKey('comics.id'))
  author_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
