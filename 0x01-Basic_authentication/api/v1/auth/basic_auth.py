import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User  # Assuming User class is defined in models.user

UserType = TypeVar('User')  # Type alias for User

class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth. """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extract Base64 part from Authorization header. """
        if not authorization_header or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

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
