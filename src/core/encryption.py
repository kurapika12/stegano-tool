# src/core/encryption.py
import os
from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """Generate a symmetric encryption key."""
    return Fernet.generate_key()


def save_key(key: bytes, filename: str = None):
    """
    Save the generated key to a file.
    If no filename is provided, saves to data/secret/key.key by default.
    """
    if filename is None:
        filename = "data/secret/key.key"

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(key)


def load_key(path: str = "data/secret/key.key") -> bytes:
    """Load encryption key from file."""
    with open(path, "rb") as f:
        return f.read()


def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypt the message using Fernet symmetric encryption."""
    return Fernet(key).encrypt(message.encode())


def decrypt_message(token: bytes, key: bytes) -> str:
    """Decrypt the encrypted message."""
    return Fernet(key).decrypt(token).decode()
