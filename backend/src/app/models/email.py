from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base 
import datetime

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(255), unique=True, index=True, nullable=False)
    subject = Column(String(512))
    sender = Column(String(255), index=True)
    recipient = Column(String(255))
    date = Column(DateTime, index=True)
    body = Column(Text)
    summary = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")