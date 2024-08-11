#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

# CORS configuration
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None  # Initialize auth variable

# Load authentication based on AUTH_TYPE environment variable
auth_type = getenv("AUTH_TYPE")
if auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def filter_request() -> None:
    """Filter each request for authentication."""
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    # Check if the request path requires authentication
    if auth.require_auth(request.path, excluded_paths):
        # Check for authorization header
        if auth.authorization_header(request) is None:
            abort(401)  # Unauthorized

        # Check for current user
        current_user = auth.current_user(request)
        if current_user is None:
            abort(403)  # Forbidden
        else:
            request.current_user = current_user


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


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
