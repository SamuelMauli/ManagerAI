from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..core.security import encrypt_data, decrypt_data
from ..services import email_service
from ..database import get_db
from ..core.security import get_current_active_user

router = APIRouter(
    prefix="/api/settings",
    tags=["Settings"],
)

@router.post("/gmail", status_code=200)
def save_gmail_settings(
    settings_in: schemas.setting.GmailSettings, # Usando um schema apropriado
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Salva ou atualiza as configurações de e-mail (Gmail) para o usuário.
    """
    try:
        # Aqui você implementaria a lógica para salvar as configs no banco de dados
        # Por exemplo, usando uma tabela 'settings'
        print(f"Salvando configuração para o e-mail: {settings_in.email}")
        email_service.update_email_config(db=db, user_id=current_user.id, config=settings_in)
        return {"message": "Configurações do Gmail salvas com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gmail", response_model=schemas.setting.GmailSettings)
def get_gmail_settings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Obtém o endereço de e-mail configurado para o usuário (a senha nunca é retornada).
    """
    config = email_service.get_email_config(db=db, user_id=current_user.id)
    return config