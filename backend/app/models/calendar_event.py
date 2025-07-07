from sqlalchemy import (Column, String, DateTime, 
                        ForeignKey, Text, Integer)
from sqlalchemy.orm import relationship
from ..database import Base

class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(String(255), primary_key=True, index=True)
    summary = Column(Text, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="calendar_events")