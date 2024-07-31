#!/usr/bin/env python3
"""Encrypt Password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
