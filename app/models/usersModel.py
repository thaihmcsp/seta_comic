from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum as SqlEnum
from .base import Base
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    premium = "premium"
    guest = "guest"

class UserStatus(str, Enum):
    pending = "pending"
    active = "active"
    deactive = "deactive"
    banned = "banned"    

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    avatar_url = Column(String)
    is_premium = Column(Boolean, default=False)
    role = Column(
        SqlEnum(UserRole, name="userrole", create_type=True),
        default=UserRole.guest
    )
    user_status = Column(
        SqlEnum(UserStatus, name="userstatus", create_type=True),
        default=UserStatus.pending
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
