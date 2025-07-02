from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..services import google
from ..utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/google/callback", response_model=schemas.Token)
def auth_google_callback(code_container: dict, db: Session = Depends(get_db)):
    code = code_container.get("code")
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O código de autorização do Google não foi fornecido."
        )

    user_info_tuple = google.exchange_code_for_credentials(code)
    if not user_info_tuple:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível obter as informações do usuário do Google. Verifique as credenciais do servidor."
        )

    user_info, credentials = user_info_tuple

    credentials_dict = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry': credentials.expiry
    }

    user = crud.get_or_create_user(db, google_info=user_info, credentials=credentials_dict)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível criar ou recuperar o usuário."
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}