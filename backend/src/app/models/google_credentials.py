from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GoogleCredentials(Base):
    __tablename__ = 'google_credentials'
    id = Column(Integer, primary_key=True)
    token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_uri = Column(Text, nullable=False)
    client_id = Column(Text, nullable=False)
    client_secret = Column(Text, nullable=False)
    scopes = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    owner = relationship("User", back_populates="google_credentials")