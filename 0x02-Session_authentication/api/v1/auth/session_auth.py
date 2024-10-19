#!/usr/bin/env python3
"""
Session authentication module
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session authentication class that inherits from Auth."""

    # Class attribute to store session ID and corresponding user ID
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a given user ID.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            str: The session ID if successful, or None if invalid input.
        """
        # Validate the user_id
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a session ID using uuid4
        session_id = str(uuid.uuid4())

        # Store the session ID with the associated user ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        # Return the session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.
        
        Args:
            session_id (str): The session ID to lookup.
        
        Returns:
            str: The user ID associated with the session ID, or None if invalid input.
        """
        # Validate the session_id
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the user ID using the .get() method on the dictionary
        return self.user_id_by_session_id.get(session_id)
