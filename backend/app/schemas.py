import datetime
from typing import Optional, List, Dict, Any
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

# NOVO: Schema para envio de e-mail
class EmailSendRequest(BaseModel):
    to: str
    subject: str
    body: str
    is_html: bool = False
    # Opcional: para responder a um email específico
    in_reply_to_id: Optional[str] = None 
    thread_id: Optional[str] = None

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

# NOVO: Schema para criação de evento no calendário
class CalendarEventCreate(BaseModel):
    summary: str
    description: Optional[str] = None
    start_time: datetime.datetime
    end_time: datetime.datetime
    time_zone: str = "America/Sao_Paulo" # Fuso horário padrão Curitiba
    attendees: Optional[List[EmailStr]] = None

# NOVO: Schema para atualização de evento no calendário
class CalendarEventUpdate(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    time_zone: Optional[str] = None
    attendees: Optional[List[EmailStr]] = None

# ==============================================================================
# Schemas de Arquivos do Drive
# ==============================================================================

# NOVO: Schema para representar um arquivo do Drive
class DriveFile(BaseModel):
    id: str
    name: str
    mime_type: str
    web_view_link: str
    created_time: datetime.datetime

# NOVO: Schema para o conteúdo de um arquivo do Drive
class DriveFileContent(BaseModel):
    file_id: str
    file_name: str
    mime_type: str
    content: str # Conteúdo do arquivo como string

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

class ChatMessage(BaseModel):
    role: str
    content: str