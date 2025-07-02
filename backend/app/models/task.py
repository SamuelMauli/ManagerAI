import datetime
from sqlalchemy import (Column, Integer, String, DateTime, 
                        ForeignKey, Text, Boolean) # Imports completos
from sqlalchemy.orm import relationship
from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    status = Column(String(100))
    project_id = Column(String(100))
    assignee = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")