from cryptography.fernet import Fernet
from app.config import settings

# Fernet works with bytes, but the key is a str, so we need the .encode() to convert str to byte.
# Instead, .decode() convert byte to str
# We declare _fernet (with underscore) to make sure the variable is encapsulated, instead the methods are usable externally
_fernet = Fernet(settings.encryption_key.encode())

def encrypt_token(token: str) -> str:
    return _fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted: str) -> str:
    return _fernet.decrypt(encrypted.encode()).decode()