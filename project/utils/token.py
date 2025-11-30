import jwt
from functools import wraps
from flask import request, jsonify
from project.models.user import User
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def verify_access_token(auth_header):
    """Extract token from 'Bearer <token>' and return user_id."""
    try:
        # Expect header format: "Bearer <token>"
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            return None

        token = parts[1]
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data["id"]  # return user id stored in token

    except Exception:
        return None



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data["id"])
        except:
            return jsonify({"error": "Token invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated
