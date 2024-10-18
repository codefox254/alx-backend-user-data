#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth to None
auth = None

# Load and assign the correct instance of authentication to auth based on AUTH_TYPE
auth_type = getenv("AUTH_TYPE", None)

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth  # Import BasicAuth
    auth = BasicAuth()  # Create an instance of BasicAuth
elif auth_type == "auth":
    from api.v1.auth.auth import Auth  # Import Auth
    auth = Auth()  # Create an instance of Auth


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


# Before request handler to validate requests
@app.before_request
def before_request_handler():
    """Handler for filtering requests before processing them."""
    if auth is None:
        return

    # Define paths that do not require authentication
    excluded_paths = [
        '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'
    ]

    # Check if the request requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Check if the Authorization header is present
    if auth.authorization_header(request) is None:
        abort(401)

    # Check if the current user is present
    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
