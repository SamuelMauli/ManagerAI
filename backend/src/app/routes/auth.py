import os
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow

from app.database import get_db
from app.models.user import User
from app.schemas.token import Token
from app.services.auth_service import create_access_token, get_password_hash # Este import agora vai funcionar

router = APIRouter()

# Configuração do fluxo OAuth do Google
# Garante que o arquivo client_secret.json esteja na raiz do backend
CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "client_secret.json")

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ],
    redirect_uri="postmessage"
)

@router.post("/google", response_model=Token)
async def auth_google(code: str = Body(..., embed=True), db: Session = Depends(get_db)):
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, google_requests.Request(), credentials.client_id
        )

        email = id_info.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not found in Google token",
            )

        user = db.query(User).filter(User.email == email).first()

        if not user:
            new_user = User(
                email=email,
                name=id_info.get("name"),
                hashed_password=get_password_hash(os.urandom(16).hex())
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user

        # Gera e retorna nosso próprio token JWT
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"Error during Google authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials with Google",
            headers={"WWW-Authenticate": "Bearer"},
        )