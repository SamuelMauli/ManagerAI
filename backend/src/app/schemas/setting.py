from pydantic import BaseModel, EmailStr
from typing import Any, Optional

class GmailSettings(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None 
class SettingBase(BaseModel):
    key: str
    value: Any

class SettingCreate(SettingBase):
    pass

class SettingUpdate(SettingBase):
    pass

class Setting(SettingBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True