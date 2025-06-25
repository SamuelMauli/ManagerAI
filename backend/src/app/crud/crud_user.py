from sqlalchemy.orm import Session
from typing import Union
from .. import models, schemas
from ..core.security import get_password_hash

class CRUDUser:
    def get_by_email(self, db: Session, *, email: str) -> Union[models.User, None]:
        return db.query(models.User).filter(models.User.email == email).first()

    def create(self, db: Session, *, obj_in: schemas.user.UserCreate) -> models.User:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = models.User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=hashed_password,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_total_user_count(self, db: Session) -> int:
        return db.query(models.User).count()

user = CRUDUser()