from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.calendar_event import CalendarEvent
from app.schemas.calendar import CalendarEventCreate, CalendarEventUpdate


class CRUDCalendarEvent(CRUDBase[CalendarEvent, CalendarEventCreate, CalendarEventUpdate]):
    def get_by_google_event_id(self, db: Session, *, google_event_id: str) -> CalendarEvent | None:
        return db.query(self.model).filter(self.model.google_event_id == google_event_id).first()


calendar_event = CRUDCalendarEvent(CalendarEvent)