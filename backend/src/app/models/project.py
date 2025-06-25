from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True)
    short_name = Column(String(50), unique=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")
    
    tasks = relationship("Task", back_populates="project")