from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class CalendarEventBase(BaseModel):
    google_event_id: str
    summary: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    html_link: Optional[str] = None
    creator_email: Optional[str] = None
    organizer_email: Optional[str] = None


class CalendarEventCreate(CalendarEventBase):
    pass


class CalendarEventUpdate(CalendarEventBase):
    pass


class CalendarEvent(CalendarEventBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)