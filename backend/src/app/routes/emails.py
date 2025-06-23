from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..models.email import Email
from ..schemas.email import Email as EmailSchema
from ..database import get_db

router = APIRouter(
    prefix="/api/emails",
    tags=["Emails"],
)

@router.get("/", response_model=List[EmailSchema])
def read_emails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all emails from the database.
    """
    emails = db.query(Email).offset(skip).limit(limit).all()
    return emails