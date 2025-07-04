import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    """Busca um usuário pelo ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """Busca um usuário pelo email."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Cria um novo usuário a partir dos dados do Google.
    Esta versão é para o fluxo OAuth e não requer senha.
    """
    db_user = models.User(
        email=user.email,
        name=user.full_name, # Mapeia 'full_name' do schema para 'name' do modelo
        picture_url=user.picture # Mapeia 'picture' do schema para 'picture_url' do modelo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def store_google_token(db: Session, token_data: schemas.GoogleTokenCreate):
    """
    ## NOVO ##
    Armazena ou atualiza o token de acesso do Google para um usuário.
    """
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    
    if not user:
        return None

    user.access_token = token_data.access_token
    user.refresh_token = token_data.refresh_token
    
    user.expires_at = datetime.datetime.fromtimestamp(token_data.expires_at, tz=datetime.timezone.utc)
    
    db.commit()
    db.refresh(user)
    
    return user

def get_or_create_user(db: Session, google_info: Dict[str, Any], credentials: Dict[str, Any]) -> models.User:
    user_email = google_info.get("email")
    db_user = get_user_by_email(db, email=user_email)

    if db_user:
        db_user.name = google_info.get("name")
        db_user.picture_url = google_info.get("picture")
        db_user.access_token = credentials.get("token")

        if not db_user.google_id:
            db_user.google_id = google_info.get("id")
        if credentials.get("refresh_token"):
            db_user.refresh_token = credentials.get("refresh_token")
        db_user.expires_at = credentials.get("expiry")
    else:
        db_user = models.User(
            email=user_email,
            name=google_info.get("name"),
            picture_url=google_info.get("picture"),
            google_id=google_info.get("id"),
            access_token=credentials.get("token"),
            refresh_token=credentials.get("refresh_token"),
            expires_at=credentials.get("expiry")
        )
        db.add(db_user)

    db.commit()
    db.refresh(db_user)
    return db_user


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
    return db.query(models.Email).filter(models.Email.google_email_id == google_email_id, models.Email.user_id == user_id).first()

def create_multiple_user_emails(db: Session, emails: list[schemas.EmailCreate], user_id: int):
    """Cria múltiplos e-mails para um usuário."""
    db_emails = [models.Email(**email.model_dump(), user_id=user_id) for email in emails]
    db.bulk_save_objects(db_emails)
    db.commit()

def mark_email_as_read(db: Session, email_id: int):
    """Marca um e-mail como lido."""
    db_email = db.query(models.Email).filter(models.Email.id == email_id).first()
    if db_email:
        db_email.is_read = True
        db.commit()
        db.refresh(db_email)
    return db_email

def get_emails_by_thread_id(db: Session, user_id: int, thread_id: str) -> List[models.Email]:
    """
    Retorna todos os e-mails de uma thread específica para um determinado usuário.
    """
    return db.query(models.Email).filter(
        models.Email.user_id == user_id,
        models.Email.thread_id == thread_id
    ).order_by(models.Email.received_at).all()


def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    """Cria uma nova tarefa para um usuário."""
    db_task = models.Task(
        **task.model_dump(), 
        user_id=user_id,
        created_at=datetime.datetime.utcnow() 
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
    update_data = task_in.model_dump(exclude_unset=True) 
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