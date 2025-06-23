from sqlalchemy import Column, Integer, String, LargeBinary
from ..database import Base 

class Setting(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True)
    value = Column(LargeBinary)