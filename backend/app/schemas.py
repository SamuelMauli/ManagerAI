from pydantic import BaseModel
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

class Task(BaseModel):
    id: int
    title: str
    status: Optional[str]
    project_id: Optional[str]
    assignee: Optional[str]
    class Config:
        orm_mode = True

class CalendarEvent(BaseModel):
    id: str
    summary: str
    start_time: datetime
    end_time: datetime
    class Config:
        orm_mode = True