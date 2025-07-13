from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from .base import Base

class Comic(Base):
  __tablename__ = 'comics'

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, unique=True, index=True)
  description = Column(String)
  cover_url = Column(String)
  is_published = Column(Boolean, default=False)
  is_banned = Column(Boolean, default=False)
  is_premium = Column(Boolean, default=False)
  slug = Column(String, unique=True, index=True)

  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  author_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
