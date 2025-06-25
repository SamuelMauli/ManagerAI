from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List

class CRUDEmail:
    def get_emails_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.Email]:
        return db.query(models.Email).filter(models.Email.owner_id == owner_id).order_by(models.Email.received_at.desc()).offset(skip).limit(limit).all()

    def get_unread_emails_count(self, db: Session, *, owner_id: int) -> int:
        # Supondo que você adicione um campo 'is_read' ao modelo Email
        return db.query(models.Email).filter(models.Email.owner_id == owner_id, models.Email.is_read == False).count()

    def get_summarized_unread_emails(self, db: Session, *, owner_id: int, limit: int = 5) -> List[models.Email]:
        return db.query(models.Email).filter(models.Email.owner_id == owner_id, models.Email.is_read == False).order_by(models.Email.received_at.desc()).limit(limit).all()

email = CRUDEmail()