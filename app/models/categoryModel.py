from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Date
from .base import Base

class Category(Base):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True, unique=True)
  slug = Column(String, index=True, unique=True)

  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Comic_Category(Base):
  __tablename__ = 'comic_categories'

  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  comic_id = Column(Integer, ForeignKey('comics.id'), primary_key=True)
  category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
