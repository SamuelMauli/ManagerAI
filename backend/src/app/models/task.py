from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from ..database import Base 
import datetime

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    youtrack_id = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    status = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    project_id = Column(String(255), ForeignKey("projects.youtrack_id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    project = relationship("Project")
    owner = relationship("User")