# backend/app/routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user

# Adicione o prefixo e tags aqui
router = APIRouter(
    prefix="/tasks", # Adicione esta linha
    tags=["tasks"]   # Adicione esta linha (opcional, mas recomendado)
)

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_user_task(db=db, task=task, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    tasks = crud.get_tasks_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
    
    updated_task = crud.update_task(db=db, db_task=db_task, task_in=task)
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
    
    crud.delete_task(db=db, task_id=task_id)
    return {"ok": True}