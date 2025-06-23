from pydantic import BaseModel, EmailStr
from typing import Optional

class SettingBase(BaseModel):
    key: str
    value: Optional[str] = None

class SettingCreate(SettingBase):
    pass

class Setting(SettingBase):
    id: int

    class Config:
        orm_mode = True

# Schema for receiving email configuration from the frontend
class EmailConfig(BaseModel):
    email: EmailStr
    credentials: str # This will be the app password or key