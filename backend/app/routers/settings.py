# backend/app/routers/settings.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..utils.security import get_current_user
import json

router = APIRouter()

@router.get("/youtrack", response_model=schemas.YouTrackSettings)
def get_youtrack_settings(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    setting = db.query(models.Setting).filter(models.Setting.user_id == current_user.id, models.Setting.key == 'youtrack').first()
    if not setting or not setting.value:
        return schemas.YouTrackSettings(url="", token="")
    return schemas.YouTrackSettings(**json.loads(setting.value))

@router.post("/youtrack", response_model=schemas.YouTrackSettings)
def save_youtrack_settings(settings: schemas.YouTrackSettings, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    setting = db.query(models.Setting).filter(models.Setting.user_id == current_user.id, models.Setting.key == 'youtrack').first()
    if not setting:
        setting = models.Setting(user_id=current_user.id, key='youtrack')
        db.add(setting)
    setting.value = settings.json()
    db.commit()
    return settings

@router.get("/email", response_model=schemas.EmailSettings)
def get_email_settings(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return schemas.EmailSettings(email=current_user.email)

@router.post("/email", response_model=schemas.EmailSettings)
def save_email_settings(settings: schemas.EmailSettings, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    user.email = settings.email
    
    if settings.password:
        app_password_setting = db.query(models.Setting).filter(models.Setting.user_id == current_user.id, models.Setting.key == 'gmail_app_password').first()
        if not app_password_setting:
            app_password_setting = models.Setting(user_id=current_user.id, key='gmail_app_password')
            db.add(app_password_setting)
        app_password_setting.value = settings.password
        
    db.commit()
    return schemas.EmailSettings(email=user.email)