#!/usr/bin/env python3
"""
BasicAuth module for managing API basic authentication.
"""

import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User

UserType = TypeVar('User')


class BasicAuth(Auth):
    """
    BasicAuth class for implementing basic authentication mechanisms.

    This class inherits from Auth and provides methods to handle basic
    authentication, such as decoding credentials and retrieving user objects.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 encoded part of the Authorization header or None.
        """
        if authorization_header is None or not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string to UTF-8.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded UTF-8 string or None if decoding fails.
        """
        if not base64_authorization_header or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user email and password from a decoded Base64 string.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string.

        Returns:
            Tuple[str, str]: A tuple containing the user email and password, or
                             (None, None) if extraction fails.
        """
        if not decoded_base64_authorization_header or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        # Split the string at the first colon only
        parts = decoded_base64_authorization_header.split(':', 1)
        if len(parts) != 2:
            return None, None
        return parts[0], parts[1]

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> UserType:
        """
        Retrieves a User instance from credentials.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            UserType: The User instance if found and credentials are valid, else None.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        user_list = User.search({'email': user_email})
        if not user_list:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> UserType:
        """
        Retrieves the User instance for the given request.

        Args:
            request: The Flask request object.

        Returns:
            UserType: The User instance or None if authentication fails.
        """
        authorization_header = self.authorization_header(request)
        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        decoded_base64_authorization_header = self.decode_base64_authorization_header(base64_authorization_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_base64_authorization_header)
        return self.user_object_from_credentials(user_email, user_pwd)
