#!/usr/bin/env python3
"""Flask app module"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    """Return a simple welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """Register a new user."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Log out a user and destroy their session."""
    # Get the session ID from cookies
    session_id = request.cookies.get('session_id')
    if not session_id:
        return make_response("Session ID not provided", 403)
    # Attempt to find the user by session ID
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        # Destroy the session
        AUTH.destroy_session(user.id)
    else:
        # User not found, respond with 403
        return make_response("Forbidden", 403)


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Log in a user and start a session."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
