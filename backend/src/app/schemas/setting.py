from pydantic import BaseModel
from typing import Any

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