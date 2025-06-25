from sqlalchemy.orm import Session
from .. import models, schemas

class CRUDChat:
    def create_chat_message(self, db: Session, *, sender: str, message: str, user_id: int) -> models.ChatMessage:
        db_obj = models.ChatMessage(
            sender=sender,
            message=message,
            owner_id=user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

chat = CRUDChat()