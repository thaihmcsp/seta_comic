from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Date
from .base import Base

class Favorite(Base):
  __tablename__ = 'favorites'

  id = Column(Integer, primary_key=True, index=True)

  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  comic_id = Column(Integer, ForeignKey('comics.id'))
  user_id = Column(Integer, ForeignKey('users.id'))
