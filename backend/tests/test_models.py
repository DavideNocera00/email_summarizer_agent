import pytest
from sqlalchemy.exc import IntegrityError

from app.models import User

def test_create_user(db):
    user = User(email="test@gmail.com")
    db.add(user)
    db.commit()

    assert user.id is not None
    assert user.email == "test@gmail.com"
    assert user.created_at is not None
    assert user.encrypted_refresh_token is None

def test_unique_email(db):
    db.add(User(email="duplicate@gmail.com"))
    db.commit()

    db.add(User(email="duplicate@gmail.com"))
    with pytest.raises(IntegrityError):
        db.commit()