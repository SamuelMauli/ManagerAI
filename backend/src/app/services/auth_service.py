from sqlalchemy.orm import Session
from typing import Optional
from ..core.security import verify_password
from ..models.user import User

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Finds a user by email and verifies their password.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user