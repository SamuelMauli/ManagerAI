from sqlalchemy import (Column, Integer, String, DateTime, 
                        ForeignKey, Text, Boolean, func)
from sqlalchemy.orm import relationship
from ..database import Base

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    google_email_id = Column(String(255), unique=True, index=True)
    thread_id = Column(String(255), index=True)
    subject = Column(Text)
    sender = Column(String(512))
    snippet = Column(Text)
    body = Column(Text)
    is_read = Column(Boolean, default=False)
    received_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="emails")