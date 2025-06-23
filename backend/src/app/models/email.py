from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .base import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(255), unique=True, index=True, nullable=False)
    sender = Column(String(255), index=True)
    subject = Column(String(512))
    body = Column(Text)
    received_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)