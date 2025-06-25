from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from .. import models, schemas
from ..crud import crud_user
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")

async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    Decodifica o token JWT para obter o usuário atual.
    """

    user = crud_user.get_by_email(db, email=username)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    user = crud.user.get_by_email(db, email=username)
    
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Verifica se o usuário atual está ativo.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user