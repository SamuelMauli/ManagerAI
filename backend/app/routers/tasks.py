# backend/app/routers/tasks.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models
from ..database import get_db
from ..utils.security import get_current_user

router = APIRouter()

@router.get("", response_model=List[schemas.Task])
def get_tasks(
    project_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    assignee: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Task).filter(models.Task.user_id == current_user.id)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    if status:
        query = query.filter(models.Task.status == status)
    if assignee:
        query = query.filter(models.Task.assignee == assignee)
    
    return query.all()

@router.get("/filters")
def get_task_filters(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Em um app real, estes dados viriam do banco após sincronização.
    # Por agora, retornaremos dados mocados.
    projects = [{"id": "PROJ1", "name": "Projeto Alpha"}, {"id": "PROJ2", "name": "Projeto Beta"}]
    statuses = ["A Fazer", "Em Progresso", "Feito"]
    assignees = [current_user.email, "outro.colega@example.com"]
    return {"projects": projects, "statuses": statuses, "assignees": assignees}