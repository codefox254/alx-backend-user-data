#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
<<<<<<< HEAD
=======
from os import getenv
>>>>>>> refs/remotes/origin/main

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

<<<<<<< HEAD
# Load and assign the correct instance of authentication to auth based on AUTH_TYPE
auth_type = getenv("AUTH_TYPE", None)

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth  # Import BasicAuth
    auth = BasicAuth()  # Create an instance of BasicAuth
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth  # Import SessionAuth
    auth = SessionAuth()  # Create an instance of SessionAuth
elif auth_type == "session_exp_auth":  # Add condition for SessionExpAuth
    from api.v1.auth.session_exp_auth import SessionExpAuth  # Import SessionExpAuth
    auth = SessionExpAuth()  # Create an instance of SessionExpAuth
elif auth_type == "auth":
    from api.v1.auth.auth import Auth  # Import Auth
    auth = Auth()  # Create an instance of Auth
=======
# Initialize auth based on AUTH_TYPE
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()
>>>>>>> refs/remotes/origin/main

@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """Unauthorized handler."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_error(error) -> str:
    """Forbidden handler."""
    return jsonify({"error": "Forbidden"}), 403

<<<<<<< HEAD
# Before request handler to validate requests
=======

>>>>>>> refs/remotes/origin/main
@app.before_request
def before_request() -> str:
    """Before Request Handler
    Requests Validation
    """
    if auth is None:
        return

    # Updated list of excluded paths to include the login route
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'  # This route should be accessible without authentication
    ]

    # Check if the request path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Ensure either the Authorization header or session cookie is present
    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)  # Abort with 401 Unauthorized if neither is present

    # Set the current user for the request
    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)  # Abort with 403 Forbidden if the user is not authenticated

    request.current_user = current_user

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
