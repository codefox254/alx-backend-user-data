#!/usr/bin/env python3
"""Auth module for managing user authentication.

This module defines the `Auth` class, which provides methods for user
registration, login validation, session management, and password resetting.
"""

from db import DB
from typing import TypeVar
from user import User
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash a password for storing securely.

    Args:
        password: The plain text password to hash.

    Returns:
        The hashed password as a string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID string.

    Returns:
        A UUID string to be used as unique identifiers.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.

    This class handles user registration, login validation, session creation,
    session destruction, password resetting, and user retrieval based on
    session tokens.
    """

    def __init__(self):
        """Initialize the Auth class with a database connection."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password.

        Args:
            email: The email address of the user to register.
            password: The plain text password of the user to register.

        Returns:
            The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user's login credentials.

        Args:
            email: The email address of the user.
            password: The plain text password of the user.

        Returns:
            True if the login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a new session for the user with the given email.

        Args:
            email: The email address of the user.

        Returns:
            The session ID for the created session.

        Returns None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> str:
        """Retrieve a user's email from their session ID.

        Args:
            session_id: The session ID associated with the user.

        Returns:
            The email of the user associated with the session ID, or None if
            no such session exists.
        """
        if session_id is None:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session, effectively logging them out.

        Args:
            user_id: The ID of the user whose session is to be destroyed.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for the user.

        Args:
            email: The email address of the user requesting a password reset.

        Returns:
            A reset password token string.

        Raises:
            ValueError: If no user is found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("No user found with the given email.")

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password using a reset token.

        Args:
            reset_token: The reset token provided for password reset.
            password: The new plain text password.

        Raises:
            ValueError: If no user is found with the given reset token.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token.")
