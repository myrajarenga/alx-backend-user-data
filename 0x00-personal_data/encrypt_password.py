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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates whether the provided password matches the hashed password.

    Args:
        hashed_password: The hashed password as a byte string.
        password: The password to be validated as a string.

    Returns:
        True if the provided password matches the hashed
    password, False otherwise.
    """
    # Convert the password to bytes (bcrypt expects bytes input)
    password_bytes = password.encode('utf-8')

    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password_bytes, hashed_password)


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    print(hash_password(password))
    print(hash_password(password))

    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))
