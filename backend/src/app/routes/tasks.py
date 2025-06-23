from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, services
from ..dependencies import get_db, get_current_active_user

router = APIRouter()

@router.post("/tasks/", response_model=schemas.task.Task)
def create_task(
    task: schemas.task.TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new task in YouTrack and saves it to the local database.
    """
    return services.task_service.create_task(db=db, task_in=task, user_id=current_user.id)


@router.get("/tasks/", response_model=List[schemas.task.Task])
def read_tasks(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_active_user),
    skip: int = 0, 
    limit: int = 100
):
    """
    Retrieve tasks for the current user.
    """
    return services.task_service.get_tasks(db=db, user_id=current_user.id, skip=skip, limit=limit)
