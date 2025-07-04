# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from httpx_oauth.clients.google import GoogleOAuth2

from .. import crud, schemas, config
from ..database import get_db
from ..utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

google_oauth_client = GoogleOAuth2(
    config.settings.GOOGLE_CLIENT_ID, 
    config.settings.GOOGLE_CLIENT_SECRET
)

@router.post("/google/callback", response_model=schemas.Token)
async def auth_google_callback(
    body: schemas.GoogleCallback,
    db: Session = Depends(get_db)
):
    try:
        token_data = await google_oauth_client.get_access_token(body.code, redirect_uri="postmessage")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token_data['access_token']}"}
            )
            response.raise_for_status()
            user_info = response.json()

        db_user = crud.get_or_create_user_from_google(db, user_info=user_info, token_data=token_data)

        app_access_token = create_access_token(data={"sub": db_user.email})
        
        return {"access_token": app_access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"ERRO INESPERADO NA AUTENTICAÇÃO: {e}")
        raise HTTPException(status_code=500, detail=str(e))