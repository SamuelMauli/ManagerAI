# backend/src/app/routes/emails.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..core.security import get_current_active_user
from ..database import get_db

router = APIRouter(
    prefix="/api/emails",
    tags=["Emails"],
)

@router.get("/", response_model=List[schemas.email.Email])
def read_emails_for_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Busca uma lista de e-mails do banco de dados para o usuário logado.
    """
    try:
        emails = crud.email.get_emails_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar os e-mails: {e}")