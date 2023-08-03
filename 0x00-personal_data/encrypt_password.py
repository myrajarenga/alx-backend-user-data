#!/usr/bin/env python3
"""
Password Encryption and Validation Module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt.

    Args:
        password: The password to be hashed.

    Returns:
        A salted, hashed password as a byte string.
    """
    password_bytes = password.encode('utf-8')

    """generating  salt and has the password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    print(hash_password(password))
    print(hash_password(password))
