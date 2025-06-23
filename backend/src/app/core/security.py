from cryptography.fernet import Fernet
from .config import settings

# Initialize Fernet with the secret key from settings
# The key must be URL-safe base64-encoded. If it's not, generate one.
# You can generate a key using: from cryptography.fernet import Fernet; Fernet.generate_key()
try:
    key = settings.SECRET_KEY.encode()
    fernet = Fernet(key)
except Exception as e:
    raise ValueError("Invalid SECRET_KEY. Please provide a URL-safe base64-encoded key.") from e

def encrypt_data(data: str) -> str:
    """Encrypts a string."""
    if not data:
        return ""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypts a string."""
    if not encrypted_data:
        return ""
    return fernet.decrypt(encrypted_data.encode()).decode()