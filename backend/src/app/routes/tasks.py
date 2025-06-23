from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, services
from ..dependencies import get_db 

router = APIRouter()

@router.post("/tasks/", response_model=schemas.task.Task)
def create_task(
    task: schemas.task.TaskCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new task in YouTrack and saves it to the local database.
    """
    return services.task_service.create_task(db=db, task_in=task) 


@router.get("/tasks/", response_model=List[schemas.task.Task])
def read_tasks(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 100
):
    """
    Retrieve tasks.
    """
    return services.task_service.get_tasks(db=db, skip=skip, limit=limit)