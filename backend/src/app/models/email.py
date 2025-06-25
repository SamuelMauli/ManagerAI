from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(512))
    sender = Column(String(255))
    body = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    received_at = Column(DateTime, index=True)
    is_read = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")