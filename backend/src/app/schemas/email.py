from pydantic import BaseModel
from datetime import datetime

class Email(BaseModel):
    id: int
    sender: str
    subject: str
    body: str
    received_at: datetime

    class Config:
        orm_mode = True