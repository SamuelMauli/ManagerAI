from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(512), index=True)
    description = Column(Text, nullable=True)
    status = Column(String(100), index=True, nullable=True)
    assignee = Column(String(255), index=True, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="tasks")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")