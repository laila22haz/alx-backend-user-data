#!/usr/bin/env python3
"""App module
"""

from flask import Flask, abort, request, redirect
from flask import jsonify
from auth import Auth
from sqlalchemy.exc import InvalidRequestError


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Bienvenue"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """users function"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except Exception:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /sessions
      Return:
        - message
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
    """ DELETE /sessions
      Return:
        - message
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    try:
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
    except Exception:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
      Return:
        - message
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ POST /reset_password
      Return:
        - message
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
    """ PUT /reset_password
      Return:
        - message
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
