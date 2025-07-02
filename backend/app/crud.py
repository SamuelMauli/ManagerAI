from sqlalchemy.orm import Session
from . import models, schemas
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