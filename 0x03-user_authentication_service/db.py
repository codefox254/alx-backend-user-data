#!/usr/bin/env python3
"""DB module for interacting with the user authentication database.

This module provides the `DB` class for interacting with the database,
including methods for adding users, querying users, and updating user
information.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import TypeVar

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """Database class for managing user data in the authentication service.

    This class provides methods to add, find, and update users in the database.
    It uses SQLAlchemy for ORM operations and manages a SQLite database.
    """

    def __init__(self):
        """Initialize a new `DB` instance.

        Sets up the database engine, creates all tables, and initializes the
        session attribute to `None`.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Lazy initialization of the session.

        Creates a new session if it hasn't been created yet.

        Returns:
            SQLAlchemy session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email: The email address of the new user.
            hashed_password: The hashed password of the new user.

        Returns:
            The newly created User object.

        Raises:
            ValueError: If email or hashed_password is empty or invalid.
        """
        if not email or not hashed_password:
            raise ValueError("Email and password cannot be empty.")
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by specific attributes.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to User
                attributes (e.g., id, email).

        Returns:
            The User object matching the provided attributes.

        Raises:
            InvalidRequestError: If any attribute is invalid.
            NoResultFound: If no user matches the query.
        """
        if not kwargs or any(x not in VALID_FIELDS for x in kwargs):
            raise InvalidRequestError("Invalid search criteria.")
        session = self._session
        try:
            return session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound("No user found with the given criteria.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes.

        Args:
            user_id: The ID of the user to update.
            **kwargs: Arbitrary keyword arguments corresponding to User
                attributes to update (e.g., email, hashed_password).

        Raises:
            ValueError: If any attribute in kwargs is invalid.
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in VALID_FIELDS:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        session.commit()
