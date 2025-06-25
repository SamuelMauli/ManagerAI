from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from .. import crud, models, schemas
from ..core.security import get_current_active_user
from ..database import get_db

class EmailBase(BaseModel):
    subject: Optional[str] = None
    sender: Optional[str] = None
    summary: Optional[str] = None

class EmailSummary(EmailBase):
    id: int

class Email(EmailBase):
    id: int
    body: Optional[str] = None
    received_at: datetime

    class Config:
        from_attributes = True