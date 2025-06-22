# src/app/models/email.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from ..database import Base
from datetime import datetime

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(255), unique=True, index=True, nullable=False)
    sender = Column(String(255), index=True)
    subject = Column(String(512))
    body = Column(Text)
    received_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True) # Para saber quando a IA processou