from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, index=True)
    test = Column(String)
