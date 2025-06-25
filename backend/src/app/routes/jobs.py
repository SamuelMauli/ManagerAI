from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from .. import services, models
from ..core.security import get_current_active_user
from ..database import get_db

router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"],
)

@router.post("/email/sync", status_code=202)
async def trigger_email_sync_job(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Inicia uma tarefa em segundo plano para buscar e armazenar os e-mails do Gmail.
    """
    background_tasks.add_task(services.email_service.fetch_and_store_emails, db=db, user_id=current_user.id)
    return {"message": "A busca de e-mails foi iniciada em segundo plano."}

@router.post("/youtrack/sync", status_code=202)
async def trigger_youtrack_sync_job(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Inicia uma tarefa em segundo plano para sincronizar todos os dados do YouTrack.
    """
    try:
        background_tasks.add_task(services.youtrack_service.sync_youtrack_data, db=db, user_id=current_user.id)
        return {"message": "A sincronização com o YouTrack foi iniciada em segundo plano."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))