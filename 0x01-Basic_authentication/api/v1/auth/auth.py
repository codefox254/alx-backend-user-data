#!/usr/bin/env python3
"""Auth module for managing API authentication."""

from typing import List, TypeVar
from flask import request
import fnmatch


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path."""
        if path is None:
            return True
        if not excluded_paths:
            return True

        # Normalize the path to ensure it ends with a slash
        if not path.endswith('/'):
            path += '/'

        # Check against each excluded path
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                # Handle exact matches or patterns ending with '/'
                if fnmatch.fnmatch(path, excluded_path):
                    return False

        return True

    
    def authorization_header(self, request=None) -> str:
        """Returns the value of the Authorization header from the request.
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    
    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user.
        """
        return None
