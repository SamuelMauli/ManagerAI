from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user
from ..services import google as google_service # Renomear para evitar conflito com googleapiclient

router = APIRouter(
    prefix="/emails",
    tags=["emails"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/sync", status_code=status.HTTP_202_ACCEPTED)
async def sync_emails_endpoint(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Inicia uma tarefa em segundo plano para sincronizar os e-mails do Google para o usuário logado.
    """
    if not current_user.access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not authenticated with Google or access token missing."
        )
    background_tasks.add(google_service.sync_google_emails, db, current_user.id)
    return {"message": "Sincronização de e-mails iniciada em segundo plano."}

@router.get("/", response_model=List[schemas.Email])
def read_emails(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retorna a lista de e-mails sincronizados para o usuário logado.
    """
    emails = crud.get_emails_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return emails

@router.get("/unread", response_model=List[schemas.EmailUnread])
def read_unread_emails(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retorna a lista de e-mails não lidos sincronizados para o usuário logado.
    """
    emails = crud.get_unread_emails_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return emails

@router.post("/{email_id}/mark_as_read", response_model=schemas.Email)
def mark_email_as_read_endpoint(
    email_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Marca um e-mail específico como lido.
    """
    db_email = crud.get_email_by_id(db, email_id=email_id)
    if not db_email:
        raise HTTPException(status_code=404, detail="Email not found")
    if db_email.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to mark this email as read")

    updated_email = crud.mark_email_as_read(db, email_id=email_id)
    return updated_email

@router.get("/{email_id}", response_model=schemas.Email)
def read_email_detail(
    email_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Retorna os detalhes de um e-mail específico.
    """
    db_email = crud.get_email_by_id(db, email_id=email_id)
    if not db_email:
        raise HTTPException(status_code=404, detail="Email not found")
    if db_email.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this email")
    return db_email