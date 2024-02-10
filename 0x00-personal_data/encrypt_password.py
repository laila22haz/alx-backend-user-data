#!/usr/bin/env python3
"""Encrypting passwords log"""
import bcrypt

def hash_password(password: str) -> bytes:
    """hash_password function"""
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return password

