# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..services import google 
from ..utils.security import create_access_token, get_current_user


router = APIRouter()

@router.post("/google", response_model=schemas.Token)
def auth_google(code_container: dict, db: Session = Depends(get_db)):
    code = code_container.get("code")
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code not found")

    user_info_tuple = google.exchange_code_for_credentials(code)
    if not user_info_tuple:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not retrieve user info from Google")

    user_info, credentials = user_info_tuple

    user = crud.get_or_create_user(db, google_info=user_info, credentials=credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create or retrieve user")

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user