# backend/app/routers/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..utils.security import get_current_user
from sqlalchemy import func

router = APIRouter()

@router.get("/project/{project_id}")
def get_project_dashboard_data(project_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Lógica de exemplo para buscar dados do dashboard
    tasks_query = db.query(models.Task).filter(
        models.Task.user_id == current_user.id, 
        models.Task.project_id == project_id
    )
    
    total_tasks = tasks_query.count()
    unresolved_tasks = tasks_query.filter(models.Task.status != 'Feito').count() # Exemplo
    
    task_counts_by_status = db.query(
        models.Task.status, func.count(models.Task.id)
    ).filter(
        models.Task.user_id == current_user.id,
        models.Task.project_id == project_id
    ).group_by(models.Task.status).all()

    formatted_counts = [{"status": status, "count": count} for status, count in task_counts_by_status]

    return {
        "total_tasks": total_tasks,
        "unresolved_tasks": unresolved_tasks,
        "task_counts_by_status": formatted_counts
    }