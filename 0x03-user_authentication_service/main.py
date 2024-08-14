#!/usr/bin/env python3
"""User Authentication Integration Test"""


import requests

BASE_URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """
    Register a new user.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Raises:
        AssertionError: If the status code or response not expected.
    """
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"
    assert response.json() == {
        "email": email,
        "message": "user created"
    }, "Unexpected response content"


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with an incorrect password.

    Args:
        email (str): The email of the user.
        password (str): The wrong password to test.

    Raises:
        AssertionError: If the status code is not as expected.
    """
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 401, \
        f"Expected status code 401, but got {response.status_code}"


def log_in(email: str, password: str) -> str:
    """
    Log in with the correct credentials.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID from the login response.

    Raises:
        AssertionError: If the status code is not as expected.
    """
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Attempt to access the profile page without being logged in.

    Raises:
        AssertionError: If the status code is not as expected.
    """
    response = requests.get(f"{BASE_URL}/auth/profile")
    assert response.status_code == 403, \
        f"Expected status code 403, but got {response.status_code}"


def profile_logged(session_id: str) -> None:
    """
    Access the profile page with a valid session ID.

    Args:
        session_id (str): The session ID of the logged-in user.

    Raises:
        AssertionError: If the status code or response content not expected.
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/auth/profile", cookies=cookies)
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"
    assert "email" in response.json(), "Expected 'email' in response"


def log_out(session_id: str) -> None:
    """
    Log out the user by invalidating the session ID.

    Args:
        session_id (str): The session ID of the logged-in user.

    Raises:
        AssertionError: If the status code is not as expected.
    """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/auth/logout", cookies=cookies)
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"


def reset_password_token(email: str) -> str:
    """
    Request a password reset token.

    Args:
        email (str): The email of the user.

    Returns:
        str: The password reset token.

    Raises:
        AssertionError: If the status code is not as expected.
    """
    response = requests.post(
        f"{BASE_URL}/auth/reset_password",
        json={"email": email}
    )
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the user's password using the reset token.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset token provided to the user.
        new_password (str): The new password to set.

    Raises:
        AssertionError: If the status code is not as expected.
    """
    response = requests.put(
        f"{BASE_URL}/auth/update_password",
        json={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200, \
        f"Expected status code 200, but got {response.status_code}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
