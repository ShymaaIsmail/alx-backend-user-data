#!/usr/bin/env python3
"""BasicAuth Module for the API"""

import base64
from api.v1.auth.auth import Auth


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
