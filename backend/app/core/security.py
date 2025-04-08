from cryptography.fernet import Fernet

from app.core.config import settings

KEY = settings.FERNET_KEY
fernet = Fernet(KEY.encode())


def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
