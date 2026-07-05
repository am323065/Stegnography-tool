# Arpita + Rakshita + Aftab & Team

"""
Module 3 - Encryption Layer
Steganography Tool

Authors: Arpita, Rakshita and Aftab
Project: Steganography Tool

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


def decrypt_message(hidden_message: str, password: str) -> str:

    if not password:
        return hidden_message

    if not hidden_message.startswith("gAAAAA"):
        raise ValueError(
            "This image contains a normal (unencrypted) message. "
            "Please decode it without entering a password."
        )

    key = _generate_key(password)
    cipher = Fernet(key)

    try:
        decrypted = cipher.decrypt(hidden_message.encode())
        return decrypted.decode()

    except InvalidToken:
        raise ValueError(
            "Incorrect password or corrupted encrypted message."
        )
