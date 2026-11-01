from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.security import encrypt_token

def insert_user(db: Session, email: str, refresh_token: str | None) -> User:
    user = db.scalar(select(User).where(User.email == email))

    if user is None:
        user = User(email = email)
        db.add(user)

    if refresh_token is not None:
        user.encrypted_refresh_token = encrypt_token(refresh_token)

    db.commit()
    db.refresh(user)
    return user