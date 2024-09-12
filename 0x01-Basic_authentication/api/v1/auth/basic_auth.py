#!/usr/bin/env python3
"""
BasicAuth module for managing API basic authentication.
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


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
        """ Decode Base64 string to UTF-8. """
        if not base64_authorization_header or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user email and password from decoded Base64 string. """
        if not decoded_base64_authorization_header or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        # Split the string at the first colon only
        parts = decoded_base64_authorization_header.split(':', 1)
        if len(parts) != 2:
            return None, None
        return parts[0], parts[1]

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> UserType:
        """ Retrieve User instance from credentials. """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        user_list = User.search(user_email)  # Assuming User.search() is a class method to find users by email
        if not user_list:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):  # Assuming User.is_valid_password() checks the password
            return None
        return user

    def current_user(self, request=None) -> UserType:
        """ Retrieve User instance for the request. """
        authorization_header = self.authorization_header(request)  # Use Auth's method to get the header
        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        decoded_base64_authorization_header = self.decode_base64_authorization_header(base64_authorization_header)
        user_email, user_pwd = self.extract_user_credentials(decoded_base64_authorization_header)
        return self.user_object_from_credentials(user_email, user_pwd)
