from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.services.calendar_service import calendar_service

router = APIRouter()

@router.post("/calendar/sync", status_code=200)
def sync_calendar(
    *,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """
    Inicia a sincronização de eventos do Google Calendar para o usuário logado.
    """
    try:
        result = calendar_service.sync_user_calendar(db, user_id=current_user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha na sincronização do calendário: {e}")