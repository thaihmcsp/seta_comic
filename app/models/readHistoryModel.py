from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Date
from .base import Base

class History(Base):
  __tablename__ = 'read_histories'

  id = Column(Integer, primary_key=True, index=True)

  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  comic_id = Column(Integer, ForeignKey('comics.id'))
  chapter_id = Column(Integer, ForeignKey('chapters.id'))
  user_id = Column(Integer, ForeignKey('users.id'))
