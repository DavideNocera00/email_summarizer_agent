import pytest
from cryptography.fernet import InvalidToken
from app.security import decrypt_token, encrypt_token

def test_encrypt_and_decrypt():
    original = "1//example-refresh-token"
    encrypted = encrypt_token(original)
    
    assert encrypted != original
    assert decrypt_token(encrypted) == original

def test_modified_token_rejection():
    encrypted = encrypt_token("secret")
    alterated = encrypted[:-2] + "xx"

    with pytest.raises(InvalidToken):
        decrypt_token(alterated)