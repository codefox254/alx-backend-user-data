#!/usr/bin/env python3
"""Flask application for user authentication service.

This module defines a Flask application with routes for user registration,
login, logout, profile viewing, and password reset functionality.
"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Handle GET requests to the root URL.

    Returns:
        A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user() -> str:
    """Handle POST requests to create a new user.

    Expects:
        - email: User's email address.
        - password: User's password.

    Returns:
        A JSON response with a success message and the user's email if created
        successfully, or an error message if the email is already registered.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Handle POST requests to log in a user.

    Expects:
        - email: User's email address.
        - password: User's password.

    Returns:
        A JSON response with a success message and the user's email if login
        is successful, or an error message if login fails.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Handle DELETE requests to log out a user.

    Returns:
        A redirection to the root URL if logout is successful, or a 403 error
        if the session ID is invalid or the user is not logged in.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """Handle GET requests to view the user's profile.

    Returns:
        A JSON response with the user's email if the session is valid,
        or a 403 error if the session ID is invalid.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Handle POST requests to get a password reset token.

    Expects:
        - email: User's email address.

    Returns:
        A JSON response with the user's email and a reset token if the email
        is valid, or a 403 error if the email is not found.
    """
    email = request.form.get('email')
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Handle PUT requests to update the user's password.

    Expects:
        - email: User's email address.
        - reset_token: Reset token received from the reset process.
        - new_password: New password for the user.

    Returns:
        A JSON response with a success message if the password is updated
        successfully, or a 403 error if the reset token is invalid.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_psw = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_psw)
        return jsonify({"email": f"{email}",
                        "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
