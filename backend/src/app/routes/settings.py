# backend/src/app/routes/settings.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..core.security import get_current_active_user
from ..database import get_db  # Importação correta

router = APIRouter(
    prefix="/api/settings",
    tags=["Settings"]
)

@router.post("/gmail", status_code=200, response_model=schemas.message.Message)
def save_gmail_settings(
    settings_in: schemas.setting.GmailSettings,
    db: Session = Depends(get_db),  # Uso correto da dependência
    current_user: models.User = Depends(get_current_active_user)
):
    try:
        crud.setting.update_setting(
            db=db, user_id=current_user.id, key="gmail_email", value=settings_in.email
        )
        # Garante que uma senha não nula seja salva
        if settings_in.password:
            crud.setting.update_setting(
                db=db, user_id=current_user.id, key="gmail_password", value=settings_in.password
            )
        return {"message": "Configurações do Gmail salvas com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar as configurações do Gmail: {e}")

@router.get("/gmail", response_model=schemas.setting.GmailSettings)
def get_gmail_settings(
    db: Session = Depends(get_db), # Uso correto da dependência
    current_user: models.User = Depends(get_current_active_user)
):
    try:
        email = crud.setting.get_setting(db=db, user_id=current_user.id, key="gmail_email")
        return schemas.setting.GmailSettings(email=email or "", password="")
    except Exception:
        return schemas.setting.GmailSettings(email="", password="")