import datetime
from sqlalchemy import (Column, Integer, String, DateTime, 
                        ForeignKey, Text, Boolean)
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    google_id = Column(String, unique=True, nullable=True)
    picture_url = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    emails = relationship("Email", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("Settings", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String(100), index=True)
    value = Column(Text)
    user = relationship("User", back_populates="settings")

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

class CalendarEvent(Base):
    # ... (sem alterações)
    __tablename__ = "calendar_events"
    id = Column(String(255), primary_key=True, index=True)
    summary = Column(Text, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="calendar_events")

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    google_email_id = Column(String, unique=True, index=True)
    thread_id = Column(String, index=True)
    subject = Column(String)
    sender = Column(String)
    snippet = Column(Text)
    body = Column(Text)
    is_read = Column(Boolean, default=False)
    received_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="emails")
