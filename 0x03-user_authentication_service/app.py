#!/usr/bin/env python3
"""Flask app module"""

from flask import Flask, jsonify, request, abort, make_response, redirect
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
        return redirect('/')
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


@app.route('/profile', methods=['GET'])
def profile():
    """Return the user's profile information."""
    # Get the session ID from cookies
    session_id = request.cookies.get('session_id')
    # Attempt to find the user by session ID
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        # Respond with user email
        return jsonify({"email": user.email}), 200
    else:
        # User not found or invalid session ID
        return make_response("Forbidden", 403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Handle password reset requests."""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return jsonify({"error": "Email not registered"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
