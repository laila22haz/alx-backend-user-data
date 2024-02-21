#!/usr/bin/env python3
"""App module
"""

from flask import Flask, abort, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
