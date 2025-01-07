"""
This module provides utilities for password hashing using bcrypt.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    """
    Provides methods for hashing and verifying passwords.
    """
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verifies a plain password against a hashed password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """
        Hashes a plain text password.
        """
        return pwd_context.hash(password)
