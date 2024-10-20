#!/usr/bin/env python3
"""Auth module for managing API authentication."""

from typing import List, Optional  # Updated import to include Optional
from flask import request
import fnmatch
import os


class Auth:
    """
    Auth class for managing API authentication and access control.

    This class provides methods to determine if a path requires authentication,
    to retrieve authorization headers, and to retrieve the current user.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that are excluded from
                                         authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None or not excluded_paths:
            return True

        # Normalize the path to ensure it ends with a slash
        if not path.endswith('/'):
            path += '/'

        # Check against each excluded path
        for excluded_path in excluded_paths:
            # Add wildcard support with '*' at the end of excluded paths
            if fnmatch.fnmatch(path, excluded_path) or \
               (excluded_path.endswith('*') and path.startswith(excluded_path[:-1])):
                return False

        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """
        Returns the value of the Authorization header from the request.

        Args:
            request (Flask.Request, optional): The Flask request object. Defaults to None.

        Returns:
            Optional[str]: The authorization header value or None if not present.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> Optional['User']:  # Use forward reference for User
        """
        Returns the current user associated with the request.

        Args:
            request (Flask.Request, optional): The Flask request object. Defaults to None.

        Returns:
            Optional[User]: The current user object or None if not authenticated.
        """
        return None

    def session_cookie(self, request=None) -> Optional[str]:  # Change return type to Optional[str]
        """
        Returns the value of the session cookie from the request.

        Args:
            request (Flask.Request, optional): The Flask request object. Defaults to None.

        Returns:
            Optional[str]: The value of the session cookie or None if not present.
        """
        if request is None:
            return None

        # Get the cookie name from the environment variable
        cookie_name = os.getenv("SESSION_NAME", "_my_session_id")

        # Return the value of the cookie from the request
        return request.cookies.get(cookie_name)
