# backend/app/routers/calendar.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..database import get_db
from ..utils.security import get_current_user

router = APIRouter()

@router.get("/events", response_model=List[schemas.CalendarEvent])
def get_calendar_events(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Esta rota retornaria os eventos que foram sincronizados e salvos no seu banco.
    events = db.query(models.CalendarEvent).filter(models.CalendarEvent.user_id == current_user.id).all()
    return events