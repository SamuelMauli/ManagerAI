from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatMessageBase(BaseModel):
    sender: str
    message: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True