from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base 

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    youtrack_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User")