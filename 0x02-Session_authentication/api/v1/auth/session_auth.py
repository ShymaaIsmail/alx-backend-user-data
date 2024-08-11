#!/usr/bin/env python3
"""SessionAuth"""

import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class that manages session authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a given user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID
        session_id = str(uuid.uuid4())

        # Store the session ID with the corresponding user_id
        self.user_id_by_session_id[session_id] = user_id

        return session_id
