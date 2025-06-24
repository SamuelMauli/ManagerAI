from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..services import email_service, youtrack_service
from ..dependencies import get_db # Import get_db a partir dos dependencies
from ..models.user import User # Import do model de User
from ..dependencies import get_current_active_user # Import para pegar o usuário logado

router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"],
)

@router.post("/email/sync", status_code=202)
async def run_email_sync_job(
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Dispara o job em background para buscar e armazenar os e-mails do Gmail.
    """
    # Passamos o 'db' e o 'user_id' para a tarefa em background
    background_tasks.add_task(email_service.fetch_and_store_emails, db=db, user_id=current_user.id)
    return {"message": "A busca de e-mails foi iniciada em segundo plano."}


@router.post("/youtrack/sync", status_code=202)
async def run_youtrack_sync_job(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Dispara o job em background para sincronizar os dados do YouTrack.
    """
    # Supondo que o youtrack_service tenha uma função de sincronização
    # Se a função não existir, ela precisará ser criada no youtrack_service.py
    # background_tasks.add_task(youtrack_service.sync_all_data, db=db, user_id=current_user.id)
    print("Função de sincronização do YouTrack chamada.") # Placeholder
    return {"message": "A sincronização com o YouTrack foi iniciada em segundo plano."}