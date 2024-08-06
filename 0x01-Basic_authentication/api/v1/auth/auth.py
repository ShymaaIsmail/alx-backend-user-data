#!/usr/bin/env python3
"""Auth Module for the API"""


import re
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
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if(re.match(excluded_path, path)):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """get authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user"""
        return None
