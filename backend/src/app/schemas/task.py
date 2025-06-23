from pydantic import BaseModel
from typing import Optional
import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_youtrack_id: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    youtrack_id: str
    status: str
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True