#!/usr/bin/env python3
"""Encrypting passwords log"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash_password function"""
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """is_valid function"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False
