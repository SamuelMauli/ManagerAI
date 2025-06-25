from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), index=True, nullable=False)
    value = Column(LargeBinary, nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")