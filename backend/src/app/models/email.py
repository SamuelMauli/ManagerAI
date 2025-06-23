from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base 

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String(255), unique=True, index=True)
    sender = Column(String(255))
    subject = Column(String(500))
    summary = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")