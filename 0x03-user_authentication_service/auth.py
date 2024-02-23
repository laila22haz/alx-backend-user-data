#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """_hash_password function"""
    pass_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pass_bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    """generate_uuid function"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """valid_login function"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """create_session function"""
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except Exception:
            NoResultFound

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        get_user_from_session_id.
        """
        if session_id is None:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """
        destroy_session.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        get_reset_password_token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update_password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
