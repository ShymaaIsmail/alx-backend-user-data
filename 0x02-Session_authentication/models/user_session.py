#!/usr/bin/env python3
""" User session module
"""


from models.base import Base
import uuid


class UserSession(Base):
    """UserSession model to manage user sessions stored in the database"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance with user_id and session_id"""
        self.user_id = kwargs.get('user_id', '')
        self.session_id = kwargs.get('session_id', str(uuid.uuid4()))
        super().__init__(*args, **kwargs)
