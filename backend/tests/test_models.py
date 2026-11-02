import pytest
from sqlalchemy.exc import IntegrityError
from app.models import Digest, DigestItem, User

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

def make_item(digest_id: int, user_id: int) -> DigestItem:
    return DigestItem(
        digest_id=digest_id,
        user_id=user_id,
        gmail_id="m1",
        sender="example@gmail.com",
        subject="Test Subject",
        summary="This is a test summary.",
        category="lavoro",
        requires_action=False
    )

def test_same_email_cannot_be_saved_twice_for_a_user(db):
    user = User(email="u@example.com")
    db.add(user)
    db.commit()

    digest = Digest(user_id=user.id, text="digest")
    db.add(digest)
    db.commit()

    db.add(make_item(digest.id, user.id))
    db.commit()

    db.add(make_item(digest.id, user.id))
    with pytest.raises(IntegrityError):
        db.commit()