# backend/src/app/routes/dashboard.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..core.security import get_current_active_user
from ..database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats", response_model=schemas.dashboard.DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Busca estatísticas agregadas (tarefas, e-mails) para o dashboard do usuário.
    """
    try:
        # A lógica para buscar as contagens agora é delegada para a camada CRUD.
        # Isso mantém a rota limpa e focada em responder à requisição.
        pending_tasks = crud.task.get_pending_tasks_count(db=db, owner_id=current_user.id)
        unread_emails = crud.email.get_unread_emails_count(db=db, owner_id=current_user.id)
        active_projects = 0 # Placeholder para contagem de projetos, se necessário

        return schemas.dashboard.DashboardStats(
            pending_tasks=pending_tasks,
            unread_emails=unread_emails,
            active_projects=active_projects,
        )
    except Exception as e:
        # Captura qualquer erro inesperado e retorna uma resposta HTTP 500 clara.
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao buscar as estatísticas: {e}")

@router.get("/summarized-emails", response_model=List[schemas.email.EmailSummary])
async def get_summarized_emails(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Busca os resumos dos últimos e-mails não lidos do usuário no banco de dados.
    """
    try:
        emails = crud.email.get_summarized_unread_emails(db=db, owner_id=current_user.id, limit=5)
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao buscar os e-mails: {e}")