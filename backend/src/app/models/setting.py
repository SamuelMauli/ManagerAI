from sqlalchemy import Column, Integer, String
from .base import Base

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True, nullable=False)
    value = Column(String(1024), nullable=True) # Value can be encrypted