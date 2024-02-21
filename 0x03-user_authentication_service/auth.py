#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """_hash_password function"""
    pass_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pass_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user function"""
        try:
            check_email = self._db.find_user_by(email=email)
            if check_email:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            password_hash = _hash_password(password)
            user = self._db.add_user(email, password_hash)
            return user
