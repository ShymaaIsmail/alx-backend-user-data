#!/usr/bin/env python3
"""Auth Module for the API"""


from typing import List, TypeVar
from flask import request, jsonify


class Auth():
    """Auth Class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check require auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """get authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user"""
        return None
