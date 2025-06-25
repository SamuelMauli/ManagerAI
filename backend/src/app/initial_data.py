from sqlalchemy.orm import Session
from . import crud, schemas
from .core.config import settings
from .database import SessionLocal

def create_first_superuser():
    """
    Cria o primeiro superusuário a partir das variáveis de ambiente
    se ele ainda não existir no banco de dados.
    """
    db = SessionLocal()
    try:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if not user:
            user_in = schemas.user.UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                full_name="Admin",
                is_superuser=True,
            )
            crud.user.create(db, obj_in=user_in)
            print("Primeiro superusuário criado com sucesso.")
        else:
            print("Superusuário já existe, pulando a criação.")
    finally:
        db.close()