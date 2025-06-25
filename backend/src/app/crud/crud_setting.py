from sqlalchemy.orm import Session
from typing import Union
from .. import models
from ..core.security import encrypt_data, decrypt_data

class CRUDSetting:
    def get_setting(self, db: Session, *, user_id: int, key: str) -> Union[str, None]:
        db_setting = db.query(models.Setting).filter(models.Setting.owner_id == user_id, models.Setting.key == key).first()
        if db_setting:
            return decrypt_data(db_setting.value)
        return None

    def update_setting(self, db: Session, *, user_id: int, key: str, value: str):
        encrypted_value = encrypt_data(value)
        db_setting = db.query(models.Setting).filter(models.Setting.owner_id == user_id, models.Setting.key == key).first()

        if db_setting:
            db_setting.value = encrypted_value
        else:
            db_setting = models.Setting(key=key, value=encrypted_value, owner_id=user_id)
            db.add(db_setting)

        db.commit()
        db.refresh(db_setting)
        return db_setting

setting = CRUDSetting()