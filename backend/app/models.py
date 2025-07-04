# backend/app/models.py

import datetime
from sqlalchemy import (Column, Integer, String, DateTime,
                        ForeignKey, Text, Boolean)
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    google_id = Column(String(255), unique=True, nullable=True)
    picture_url = Column(Text, nullable=True)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    emails = relationship("Email", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("Setting", back_populates="user", uselist=False, cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    calendar_events = relationship("CalendarEvent", back_populates="user", cascade="all, delete-orphan")

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # CORREÇÃO: Adicionado comprimento
    key = Column(String(100), index=True)
    value = Column(Text, nullable=True)
    user = relationship("User", back_populates="settings")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    # CORREÇÃO: Adicionado comprimento
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    # CORREÇÃO: Adicionado comprimento
    status = Column(String(100), nullable=True)
    project_id = Column(String(100), nullable=True)
    assignee = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")

class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    # CORREÇÃO: Adicionado comprimento
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
    # CORREÇÃO: Adicionado comprimento
    google_email_id = Column(String(255), unique=True, index=True)
    thread_id = Column(String(255), index=True)
    subject = Column(Text, nullable=True) # Text não precisa de comprimento
    sender = Column(String(255))
    snippet = Column(Text, nullable=True)
    body = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    received_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="emails")