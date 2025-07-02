from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.services.google_service import get_gmail_service

router = APIRouter()

@router.post("/gmail", status_code=200, response_model=schemas.message.Message)
def test_gmail_connection(db: Session = Depends(get_db)):
    """
    Testa a conexão com a API do Gmail.
    """
    service = get_gmail_service()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Não foi possível autenticar com o serviço do Gmail. Verifique as credenciais no servidor."
        )

    try:
        profile = service.users().getProfile(userId='me').execute()
        email = profile.get('emailAddress')
        return {"message": f"Conexão com o Gmail bem-sucedida para o usuário: {email}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao comunicar com o Gmail: {e}"
        )

@router.get("/", status_code=status.HTTP_200_OK)
def get_settings():
    return {"message": "Endpoint de configurações está ativo."}