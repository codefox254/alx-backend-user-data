#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import session_auth_view  # Import the session authentication view

# Register the session authentication blueprint
app_views.register_blueprint(session_auth_view)

# Load User data from file
User.load_from_file()
