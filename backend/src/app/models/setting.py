from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from .. import crud, models, schemas
from ..core.security import get_current_active_user
from ..database import get_db

from .. import crud, models, schemas
from ..core.security import get_current_active_user
from ..database import get_db

class Setting(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), index=True, nullable=False)
    value = Column(LargeBinary)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User")

    __table_args__ = (
        UniqueConstraint('owner_id', 'key', name='_owner_key_uc'),
    )