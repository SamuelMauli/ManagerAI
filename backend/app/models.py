import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text 
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    
    # Corrigido: Permitir que a senha e tokens sejam nulos
    hashed_password = Column(String(255), nullable=True) 
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)

class Setting(Base):
    # ... (sem alterações)
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String(100), index=True)
    value = Column(Text)
    user = relationship("User")

class Task(Base):
    # ... (sem alterações)
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    status = Column(String(100))
    project_id = Column(String(100))
    assignee = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class CalendarEvent(Base):
    # ... (sem alterações)
    __tablename__ = "calendar_events"
    id = Column(String(255), primary_key=True, index=True)
    summary = Column(Text, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email_id = Column(String(255), unique=True, index=True) # ID do email no Gmail - Aumente se necessário
    thread_id = Column(String(255), index=True) # ID da thread do email no Gmail
    subject = Column(String(500)) # Assunto do email
    sender = Column(String(255)) # Remetente do email
    snippet = Column(Text) # Trecho do email - Mude para Text
    body = Column(Text) # Corpo do email - Mude para Text
    received_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_read = Column(Boolean, default=False)

    owner = relationship("User", back_populates="emails")