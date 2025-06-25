from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmailBase(BaseModel):
    subject: Optional[str] = None
    sender: Optional[str] = None
    body: Optional[str] = None
    summary: Optional[str] = None
    received_at: Optional[datetime] = None

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class EmailSummary(BaseModel):
    id: int
    subject: Optional[str] = None
    sender: Optional[str] = None
    summary: Optional[str] = None

    class Config:
        from_attributes = True