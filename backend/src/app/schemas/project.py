# backend/src/app/schemas/project.py

from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    short_name: str
    external_id: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True