import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# ==============================================================================
# Schemas de Autenticação
# ==============================================================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

# ==============================================================================
# Schemas de Usuário
# ==============================================================================

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    picture_url: Optional[str] = None

class UserCreate(UserBase):
    google_id: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime.datetime

class User(UserBase):
    id: int
    google_id: Optional[str] = None
    
    class Config:
        from_attributes = True

# ==============================================================================
# Schemas de Tarefas (Tasks)
# ==============================================================================

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# ==============================================================================
# Schemas de Email
# ==============================================================================

class EmailBase(BaseModel):
    google_email_id: str
    thread_id: str
    subject: Optional[str] = None
    sender: str
    snippet: Optional[str] = None
    body: Optional[str] = None
    is_read: bool = False
    received_at: datetime.datetime

class EmailCreate(EmailBase):
    pass

class Email(EmailBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# --- CORREÇÃO AQUI: ADICIONANDO O SCHEMA DE VOLTA ---
class EmailUnread(BaseModel):
    id: int
    google_email_id: str
    thread_id: str
    subject: Optional[str] = None
    sender: str
    snippet: Optional[str] = None
    received_at: datetime.datetime
    is_read: bool

    class Config:
        from_attributes = True
# ----------------------------------------------------

# ==============================================================================
# Schemas de Eventos do Calendário
# ==============================================================================

class CalendarEvent(BaseModel):
    id: str
    summary: str
    start_time: datetime.datetime
    end_time: datetime.datetime

    class Config:
        from_attributes = True

# ==============================================================================
# Schemas de Configurações e Serviços
# ==============================================================================

class Setting(BaseModel):
    key: str
    value: dict

class YouTrackSettings(BaseModel):
    url: str
    token: str

class EmailSettings(BaseModel):
    email: EmailStr
    password: Optional[str] = None

# ==============================================================================
# Schemas para Interações com IA (Chat/Reports)
# ==============================================================================

class ReportRequest(BaseModel):
    project_id: str
    user_prompt: str

class ReportResponse(BaseModel):
    content: str

class ChatResponse(BaseModel):
    content: str