#!/usr/bin/env python3
"""
Session Authentication Routes
"""

from flask import jsonify, request, make_response
from models.user import User
from api.v1.app import auth  # Import auth here to avoid circular import
from os import getenv
from flask import Blueprint

session_auth_view = Blueprint('session_auth_view', __name__)


@session_auth_view.route('/auth_session/login/', methods=['POST'], strict_slashes=False)
@session_auth_view.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles user login and session creation."""
    
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate the email parameter
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate the password parameter
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on the email
    user = User.search(email=email)
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if the provided password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the User ID
    session_id = auth.create_session(user.id)

    # Create a response and set the session cookie
    response = make_response(user.to_json())
    cookie_name = getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(cookie_name, session_id)

    return response
