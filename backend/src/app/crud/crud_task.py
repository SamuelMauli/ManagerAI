from sqlalchemy.orm import Session
from sqlalchemy import distinct
from .. import models, schemas
from typing import List, Optional, Dict, Any, Union

class CRUDTask:
    def get_by_external_id(self, db: Session, *, external_id: str, owner_id: int) -> Union[models.Task, None]:
        return db.query(models.Task).filter(models.Task.external_id == external_id, models.Task.owner_id == owner_id).first()

    def create_or_update_task(self, db: Session, *, task_in: schemas.task.TaskCreate, owner_id: int) -> models.Task:
        db_task = self.get_by_external_id(db, external_id=task_in.external_id, owner_id=owner_id)
        if db_task:
            update_data = task_in.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
        else:
            db_task = models.Task(**task_in.model_dump(), owner_id=owner_id)
            db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def get_tasks_with_filters(self, db: Session, *, owner_id: int, filters: Dict[str, Any]) -> List[models.Task]:
        query = db.query(models.Task).filter(models.Task.owner_id == owner_id)
        
        if filters.get("project_id"):
            query = query.filter(models.Task.project_id == filters["project_id"])
        if filters.get("status"):
            query = query.filter(models.Task.status == filters["status"])
        if filters.get("assignee"):
            query = query.filter(models.Task.assignee == filters["assignee"])
            
        return query.order_by(models.Task.updated_at.desc()).all()

    def get_pending_tasks_count(self, db: Session, *, owner_id: int) -> int:
        return db.query(models.Task).filter(models.Task.owner_id == owner_id, models.Task.status != "Done").count()

    def get_distinct_statuses(self, db: Session, *, owner_id: int) -> List[str]:
        results = db.query(distinct(models.Task.status)).filter(models.Task.owner_id == owner_id, models.Task.status.isnot(None)).all()
        return [result[0] for result in results]

    def get_distinct_assignees(self, db: Session, *, owner_id: int) -> List[str]:
        results = db.query(distinct(models.Task.assignee)).filter(models.Task.owner_id == owner_id, models.Task.assignee.isnot(None)).all()
        return [result[0] for result in results]
   
    def get_tasks_by_project_id(self, db: Session, *, project_id: str, owner_id: int) -> list[Task]:
        return db.query(self.model).filter(
            self.model.project_id == project_id, 
            self.model.owner_id == owner_id
        ).all()

task = CRUDTask(Task)
