from app.crud import insert_user
from app.security import decrypt_token

def test_insert_user_with_token(db):
    user = insert_user(db, "example@gmail.com", "refresh_token-123")

    assert user.id is not None
    assert user.encrypted_refresh_token != "refresh_token-123"
    assert decrypt_token(user.encrypted_refresh_token) == "refresh_token-123"

def test_update_existing_user(db):
    firstUser = insert_user(db, "example@gmail.com", "old_token")
    secondUser = insert_user(db, "example@gmail.com", "new_token")

    assert secondUser.id == firstUser.id
    assert decrypt_token(secondUser.encrypted_refresh_token) == "new_token"

def test_with_NoneToken(db):
    insert_user(db, "example@gmail.com", "refresh_token")
    user = insert_user(db, "example@gmail.com", None)

    assert decrypt_token(user.encrypted_refresh_token) == "refresh_token"