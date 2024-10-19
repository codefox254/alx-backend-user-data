#!/usr/bin/env python3
"""
Session authentication module
"""

import uuid
from api.v1.auth.auth import Auth
from models.user import User  # Assuming User model is in models/user.py


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

    def current_user(self, request=None):
        """
        Returns the current user associated with the request based on the session cookie.

        Args:
            request (Flask.Request, optional): The Flask request object. Defaults to None.

        Returns:
            User: The current user object or None if not authenticated.
        """
        if request is None:
            return None

        # Get the session cookie value
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # Get the user ID from the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Retrieve the User instance from the database
        return User.get(user_id)  # Adjust this line based on your actual User model method for retrieval

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session / logout.

        Args:
            request (Flask.Request, optional): The Flask request object. Defaults to None.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False

        # Check if the session ID cookie exists
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        # Remove the session ID from the dictionary
        del self.user_id_by_session_id[session_id]
        return True
