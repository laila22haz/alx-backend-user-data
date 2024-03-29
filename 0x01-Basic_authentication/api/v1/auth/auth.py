#!/usr/bin/env python3
"""Auth Class"""
from flask import request, Flask
from typing import List, TypeVar
import os


class Auth():
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth function"""
        check = path
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            check += "/"
        if check in excluded_paths or path in excluded_paths:
            return False
        return True


    def authorization_header(self, request=None) -> str:
        """authorization_header function"""
        if request is None:
            return None
        return request.headers.get("Authorization")


    def current_user(self, request=None) -> TypeVar('User'):
        """current_user function"""
        return None
