import datetime
from fastapi import APIRouter, Depends, HTTPException, status
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
        events = google_service.get_events_for_today(db, user=current_user)
        return events
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Falha ao buscar eventos do calendário: {str(e)}"
        )

# NOVO: Endpoint para criar evento no calendário
@router.post("/events", response_model=schemas.CalendarEvent, status_code=status.HTTP_201_CREATED)
def create_calendar_event_endpoint(
    event_data: schemas.CalendarEventCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Cria um novo evento no Google Calendar do usuário logado.
    """
    try:
        created_event = google_service.create_calendar_event(db, current_user, event_data)
        # O ID do evento do Google Calendar é uma string, não um int auto-gerado do DB.
        # Precisamos mapear a resposta da API do Google para o nosso schema.
        return schemas.CalendarEvent(
            id=created_event['id'],
            summary=created_event['summary'],
            start_time=datetime.datetime.fromisoformat(created_event['start']['dateTime']),
            end_time=datetime.datetime.fromisoformat(created_event['end']['dateTime']),
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# NOVO: Endpoint para editar evento no calendário
@router.put("/events/{event_id}", response_model=schemas.CalendarEvent)
def update_calendar_event_endpoint(
    event_id: str,
    event_data: schemas.CalendarEventUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Atualiza um evento existente no Google Calendar do usuário logado.
    """
    try:
        updated_event = google_service.update_calendar_event(db, current_user, event_id, event_data)
        return schemas.CalendarEvent(
            id=updated_event['id'],
            summary=updated_event['summary'],
            start_time=datetime.datetime.fromisoformat(updated_event['start']['dateTime']),
            end_time=datetime.datetime.fromisoformat(updated_event['end']['dateTime']),
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))