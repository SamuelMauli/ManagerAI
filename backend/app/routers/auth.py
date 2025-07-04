# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
import datetime
import time # Import the time module

from httpx_oauth.clients.google import GoogleOAuth2
from ..config import settings
from .. import crud, schemas
from ..database import get_db
from ..utils.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

google_oauth_client = GoogleOAuth2(
    settings.GOOGLE_CLIENT_ID,
    settings.GOOGLE_CLIENT_SECRET
)

@router.post("/google/callback", response_model=schemas.Token)
async def auth_google_callback(
    body: schemas.GoogleCallback,
    db: Session = Depends(get_db)
):
    try:
        # 1. Exchange the code for a token from Google
        token_data = await google_oauth_client.get_access_token(
            body.code,
            redirect_uri="postmessage"
        )
        access_token = token_data['access_token']

        # 2. Get user info from the Google API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            user_info = response.json()

        user_email = user_info.get("email")
        if not user_email:
            raise HTTPException(status_code=400, detail="Email not found in Google profile.")

        # 3. Find or create the user in your database
        db_user = crud.get_user_by_email(db, email=user_email)
        if not db_user:
            user_create_data = schemas.UserCreate(
                email=user_email,
                full_name=user_info.get("name"),
                picture=user_info.get("picture")
            )
            db_user = crud.create_user(db, user=user_create_data)

        # 4. Store the Google token details
        # ## THIS IS THE FIX ##
        # The 'expires_at' from Google is a relative timestamp in seconds.
        # We convert it to an absolute Unix timestamp (integer).
        expires_at_timestamp = int(time.time()) + token_data['expires_in']

        google_token_data = schemas.GoogleTokenCreate(
            access_token=access_token,
            refresh_token=token_data.get("refresh_token"),
            expires_at=expires_at_timestamp, # Pass the integer timestamp
            user_id=db_user.id
        )
        crud.store_google_token(db, token_data=google_token_data)

        # 5. Create your app's own JWT
        app_access_token = create_access_token(data={"sub": db_user.email})

        return {"access_token": app_access_token, "token_type": "bearer"}

    except httpx.HTTPStatusError as e:
        error_details = e.response.json()
        print(f"ERROR FROM GOOGLE: {error_details}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to validate with Google: {error_details.get('error_description', 'Invalid code')}"
        )
    except Exception as e:
        print(f"UNEXPECTED ERROR IN AUTH: {e}")
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")