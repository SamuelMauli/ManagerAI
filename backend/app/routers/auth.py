# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..services import google
from ..utils.security import create_access_token

router = APIRouter()

@router.post("/google", response_model=schemas.Token)
def auth_google(code_container: dict, db: Session = Depends(get_db)):
    """
    Recebe o código de autorização do frontend, troca por credenciais do Google,
    e cria ou atualiza o usuário no banco, retornando um token JWT para a sessão.
    """
    code = code_container.get("code")
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O código de autorização do Google não foi fornecido."
        )

    # A função exchange_code_for_credentials agora retorna as informações do usuário e as credenciais
    user_info_tuple = google.exchange_code_for_credentials(code)
    if not user_info_tuple:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível obter as informações do usuário do Google. Verifique as credenciais do servidor."
        )

    user_info, credentials = user_info_tuple

    # get_or_create_user lida com a lógica de banco de dados
    user = crud.get_or_create_user(db, google_info=user_info, credentials=credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível criar ou recuperar o usuário."
        )

    # Cria um token de acesso para a nossa aplicação
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}