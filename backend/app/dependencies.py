from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional

from .database import SessionLocal
from . import crud, models, schemas
from .config import settings
from .utils.security import verify_password, get_password_hash # Importa do utils/security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    """Dependency para obter a sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um token de acesso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """Verifica e decodifica um token JWT."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Retorna o usuário logado a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = crud.get_user(db, user_id=token_data.id)
    if user is None:
        raise credentials_exception
    return user

async def authenticate_user(db: Session, username: str, password: str):
    """Autentica um usuário usando email e senha."""
    user = crud.get_user_by_email(db, email=username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user