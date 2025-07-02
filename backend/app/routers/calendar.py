import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..dependencies import get_current_user
from ..services import google as google_service

router = APIRouter(
    prefix="/calendar",
    tags=["calendar"]
)

@router.get("/events", response_model=List[schemas.CalendarEvent])
def get_calendar_events(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Esta rota retornaria os eventos que foram sincronizados e salvos no seu banco.
    events = db.query(models.CalendarEvent).filter(models.CalendarEvent.user_id == current_user.id).all()
    return events

@router.get("/today", response_model=List[schemas.CalendarEvent])
def get_today_events(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Busca e retorna os eventos do calendário do Google para o dia atual.
    """
    try:
        # A função de serviço para buscar eventos precisa ser implementada em google.py
        events = google_service.get_events_for_today(db, user=current_user)
        return events
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Falha ao buscar eventos do calendário: {str(e)}"
        )