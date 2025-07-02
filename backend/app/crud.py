import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas
from typing import List, Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Função nova para lidar com o login do Google
def get_or_create_user(db: Session, google_info: dict, credentials):
    user = get_user_by_email(db, email=google_info['email'])
    
    if user:
        # Atualiza os tokens caso o usuário já exista e esteja logando novamente
        user.google_id = google_info.get('id')
        user.access_token = credentials.token
        user.refresh_token = credentials.refresh_token
        db.commit()
        db.refresh(user)
        return user
    
    # Cria um novo usuário se ele não for encontrado
    new_user = models.User(
        email=google_info['email'],
        google_id=google_info.get('id'),
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
        hashed_password=None # Sem senha local
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_user_email(db: Session, email: schemas.EmailCreate, user_id: int):
    db_email = models.Email(
        **email.dict(),
        user_id=user_id,
        received_at=datetime.datetime.utcnow() # Garante que received_at é definido
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def get_emails_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Email).filter(models.Email.user_id == user_id).order_by(desc(models.Email.received_at)).offset(skip).limit(limit).all()

def get_unread_emails_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Email).filter(
        models.Email.user_id == user_id,
        models.Email.is_read == False
    ).order_by(desc(models.Email.received_at)).offset(skip).limit(limit).all()

def get_email_by_id(db: Session, email_id: int):
    return db.query(models.Email).filter(models.Email.id == email_id).first()

def get_email_by_google_id(db: Session, google_email_id: str, user_id: int):
    return db.query(models.Email).filter(models.Email.email_id == google_email_id, models.Email.user_id == user_id).first()

def mark_email_as_read(db: Session, email_id: int):
    db_email = db.query(models.Email).filter(models.Email.id == email_id).first()
    if db_email:
        db_email.is_read = True
        db.commit()
        db.refresh(db_email)
    return db_email

# Adicione esta função para buscar emails por thread_id
def get_emails_by_thread_id(db: Session, user_id: int, thread_id: str):
    return db.query(models.Email).filter(
        models.Email.user_id == user_id,
        models.Email.thread_id == thread_id
    ).order_by(models.Email.received_at).all()