# backend/src/app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db

router = APIRouter()

# Exemplo de rota de usuários
@router.get("/", response_model=List[schemas.user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Lógica para buscar usuários aqui (precisa ser implementada)
    # Ex: users = db.query(models.User).offset(skip).limit(limit).all()
    # return users
    return [] # Retorna lista vazia por enquanto