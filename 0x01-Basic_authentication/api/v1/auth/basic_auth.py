#!/usr/bin/env python3
"""BasicAuth Module for the API"""

import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Auth Class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the Base64 part of the Auth header for Basic Auth."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
                                    self,
                                    base64_authorization_header: str) -> str:
        """Decode a Base64 string and return the UTF-8 decoded value."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
                                self,
                                decoded_base64_authorization_header:
                                str) -> (str, str):
        """Extract user email and password from the Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(
                                    self, user_email: str,
                                    user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user = User.search(user_email)
        if user is None:
            return None

        if not user[0].is_valid_password(user_pwd):
            return None

        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request."""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_email, user_pwd)
