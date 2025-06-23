from pydantic import BaseModel
import datetime

class ChatMessageBase(BaseModel):
    message: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    sender: str
    timestamp: datetime
    
    class Config:
        from_attributes = True
