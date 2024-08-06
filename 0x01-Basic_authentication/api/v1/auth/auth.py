#!/usr/bin/env python3
"""Auth Module for the API"""


from typing import List, TypeVar
from flask import request, jsonify


class Auth():
    """Auth Class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if the path requires authentication"""
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Normalize path to ensure consistency (remove trailing slash)
        if path[-1] != '/':
            path += '/'

        # Check if the path is in the list of excluded paths
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """get authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user"""
        return None
