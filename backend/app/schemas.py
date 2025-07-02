import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class Setting(BaseModel):
    key: str
    value: dict

class YouTrackSettings(BaseModel):
    url: str
    token: str

class EmailSettings(BaseModel):
    email: str
    password: Optional[str] = None

class ReportRequest(BaseModel):
    project_id: str
    user_prompt: str

class ReportResponse(BaseModel):
    content: str

class ChatResponse(BaseModel):
    content: str

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    # Permite que todos os campos sejam opcionais para atualização parcial
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True # Ou orm_mode = True para Pydantic V1

class CalendarEvent(BaseModel):
    id: str
    summary: str
    start_time: datetime
    end_time: datetime
    class Config:
        orm_mode = True

class EmailBase(BaseModel):
    email_id: str
    thread_id: str
    subject: Optional[str] = None
    sender: str
    snippet: Optional[str] = None
    body: Optional[str] = None
    is_read: bool = False

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    user_id: int
    received_at: datetime # Mude de datetime.datetime para apenas datetime

    class Config:
        from_attributes = True

# Esquema para EmailUnread (ajuste conforme necessário para exibir na lista)
class EmailUnread(BaseModel):
    id: int
    email_id: str
    thread_id: str
    subject: Optional[str] = None
    sender: str
    snippet: Optional[str] = None
    received_at: datetime # Mude de datetime.datetime para apenas datetime
    is_read: bool

    class Config:
        from_attributes = True