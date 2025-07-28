import uuid
from .base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())