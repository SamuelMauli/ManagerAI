from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, services
from ..database import get_db

router = APIRouter(
    prefix="/api/settings",
    tags=["Settings"],
)

@router.post("/email", status_code=200)
def update_email_settings(
    config: schemas.setting.EmailConfig, 
    db: Session = Depends(get_db)
):
    """
    Update email account configuration.
    Stores the email and encrypted credentials.
    """
    try:
        return services.email_service.update_email_config(db, config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/email", response_model=dict)
def get_email_settings(db: Session = Depends(get_db)):
    """
    Get the configured email address (credentials are not returned).
    """
    config = services.email_service.get_email_config(db)
    return {"email": config.get("email")}