from sqlalchemy.orm import Session
from typing import Union
from .. import models, schemas

class CRUDProject:
    def get_by_short_name(self, db: Session, *, short_name: str, owner_id: int) -> Union[models.Project, None]:
        return db.query(models.Project).filter(models.Project.short_name == short_name, models.Project.owner_id == owner_id).first()

    def create_or_update_project(self, db: Session, *, project_in: schemas.project.ProjectCreate, owner_id: int) -> models.Project:
        db_project = self.get_by_short_name(db, short_name=project_in.short_name, owner_id=owner_id)
        if db_project:
            db_project.name = project_in.name
        else:
            db_project = models.Project(**project_in.model_dump(), owner_id=owner_id)
            db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    def get_projects_by_owner(self, db: Session, *, owner_id: int) -> list[models.Project]:
        return db.query(models.Project).filter(models.Project.owner_id == owner_id).all()

project = CRUDProject()