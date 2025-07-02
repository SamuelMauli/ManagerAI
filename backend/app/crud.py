import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from . import models, schemas # Certifique-se de que models e schemas são importados


# --- Funções CRUD para Usuários (User) ---
def get_user(db: Session, user_id: int):
    """Busca um usuário pelo ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Busca um usuário pelo e-mail."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    """Cria um novo usuário."""
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_or_create_user(db: Session, google_info: dict, credentials):
    """Busca ou cria um usuário com base nas informações do Google."""
    user = get_user_by_email(db, email=google_info['email'])
    
    if user:
        # Atualiza os tokens caso o usuário já exista
        user.google_id = google_info.get('id')
        user.access_token = credentials.token
        user.refresh_token = credentials.refresh_token
        if hasattr(credentials, 'expiry'): # Verifica se 'expiry' existe antes de atribuir
            user.expires_at = credentials.expiry
        db.add(user) # Adicionado para garantir que as alterações sejam staged
        db.commit()
        db.refresh(user)
        return user
    
    # Cria um novo usuário se ele não for encontrado
    new_user = models.User(
        email=google_info['email'],
        google_id=google_info.get('id'),
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
        expires_at=credentials.expiry if hasattr(credentials, 'expiry') else None, # Salva a expiração
        hashed_password=None # Usuários do Google não têm senha local
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# --- Funções CRUD para E-mails (Email) ---
def create_user_email(db: Session, email: schemas.EmailCreate, user_id: int):
    """Cria um novo e-mail para um usuário."""
    db_email = models.Email(
        **email.model_dump(), # Use model_dump() para Pydantic V2
        user_id=user_id,
        received_at=datetime.datetime.utcnow()
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def get_emails_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Retorna todos os e-mails de um usuário."""
    return db.query(models.Email).filter(models.Email.user_id == user_id).order_by(desc(models.Email.received_at)).offset(skip).limit(limit).all()

def get_unread_emails_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Retorna e-mails não lidos de um usuário."""
    return db.query(models.Email).filter(
        models.Email.user_id == user_id,
        models.Email.is_read == False
    ).order_by(desc(models.Email.received_at)).offset(skip).limit(limit).all()

def get_email_by_id(db: Session, email_id: int):
    """Retorna um e-mail pelo ID do banco de dados."""
    return db.query(models.Email).filter(models.Email.id == email_id).first()

def get_email_by_google_id(db: Session, google_email_id: str, user_id: int):
    """Retorna um e-mail pelo ID do Google."""
    return db.query(models.Email).filter(models.Email.email_id == google_email_id, models.Email.user_id == user_id).first()

def mark_email_as_read(db: Session, email_id: int):
    """Marca um e-mail como lido."""
    db_email = db.query(models.Email).filter(models.Email.id == email_id).first()
    if db_email:
        db_email.is_read = True
        db.commit()
        db.refresh(db_email)
    return db_email

def get_emails_by_thread_id(db: Session, user_id: int, thread_id: str):
    """Retorna e-mails de uma thread específica."""
    return db.query(models.Email).filter(
        models.Email.user_id == user_id,
        models.Email.thread_id == thread_id
    ).order_by(models.Email.received_at).all()


# --- Funções CRUD para Tarefas (Task) ---
def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    """Cria uma nova tarefa para um usuário."""
    db_task = models.Task(
        **task.model_dump(), # Use model_dump() para Pydantic V2
        user_id=user_id,
        created_at=datetime.datetime.utcnow() # Define a data de criação
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Retorna todas as tarefas de um usuário."""
    return db.query(models.Task).filter(models.Task.user_id == user_id).order_by(desc(models.Task.created_at)).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    """Retorna uma tarefa pelo ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, db_task: models.Task, task_in: schemas.TaskUpdate):
    """Atualiza uma tarefa existente."""
    update_data = task_in.model_dump(exclude_unset=True) # Use model_dump() para Pydantic V2
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    """Deleta uma tarefa."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task