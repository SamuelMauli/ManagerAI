from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, models, schemas
from ..core.security import get_current_active_user
from ..database import get_db

router = APIRouter(
    tags=["Tasks"]
)

@router.get("/projects", response_model=List[schemas.project.Project])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """ Busca todos os projetos do usuário logado. """
    return crud.project.get_projects_by_owner(db, owner_id=current_user.id)

@router.get("/tasks", response_model=List[schemas.task.Task])
def get_tasks_with_filters(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    assignee: Optional[str] = Query(None)
):
    """ Busca tarefas com base nos filtros fornecidos. """
    filters = {
        "project_id": project_id,
        "status": status,
        "assignee": assignee
    }
    return crud.task.get_tasks_with_filters(db, owner_id=current_user.id, filters=filters)
    
@router.get("/tasks/statuses", response_model=List[str])
def get_task_statuses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """ Retorna uma lista de todos os status de tarefas distintos. """
    return crud.task.get_distinct_statuses(db, owner_id=current_user.id)

@router.get("/tasks/assignees", response_model=List[str])
def get_task_assignees(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """ Retorna uma lista de todos os responsáveis (assignees) distintos. """
    return crud.task.get_distinct_assignees(db, owner_id=current_user.id)