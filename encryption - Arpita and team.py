"""
Module 3 - Encryption Layer
Steganography Tool

This module provides optional password-based encryption and decryption
for secret messages before they are embedded into an image.

"""

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken


def _generate_key(password: str) -> bytes:
    password_hash = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(password_hash)


def encrypt_message(message: str, password: str) -> str:

    if not password:
        return message

    key = _generate_key(password)
    cipher = Fernet(key)

    encrypted = cipher.encrypt(message.encode())

    return encrypted.decode()


def decrypt_message(encrypted_message: str, password: str) -> str:

    if not password:
        return encrypted_message

    key = _generate_key(password)
    cipher = Fernet(key)

    try:
        decrypted = cipher.decrypt(encrypted_message.encode())
        return decrypted.decode()

    except InvalidToken:
        raise ValueError("Incorrect password or corrupted encrypted message.")