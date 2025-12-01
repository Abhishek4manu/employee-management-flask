from flask import Blueprint, request, jsonify
from project.models.user import User
from project.schemas.user_schema import RegisterSchema
from project import db
import jwt
import datetime

auth_bp = Blueprint("auth_bp", __name__)

import os
SECRET_KEY = os.environ.get("SECRET_KEY")


# -----------------------------
# REGISTER
# -----------------------------
@auth_bp.post("/register")
def register():
    schema = RegisterSchema()

    try:
        data = schema.load(request.json)
    except Exception as e:
        return {"error": str(e)}, 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username & password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 409

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"}), 201


# -----------------------------
# LOGIN
# -----------------------------
@auth_bp.post("/login")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token
    token = jwt.encode({
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})
