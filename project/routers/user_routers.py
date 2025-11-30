from flask import Blueprint, request, jsonify
from project import db
from project.models.user import User
from project.utils.token import token_required
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user_bp", __name__)


# -------------------------------
# GET /me  → profile of logged-in user
# -------------------------------
@user_bp.get("/me")
@token_required
def get_profile(current_user):
    data = {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }
    return jsonify(data), 200


# -------------------------------
# PATCH /me  → update own username/password
# -------------------------------
@user_bp.patch("/me")
@token_required
def update_profile(current_user):
    payload = request.get_json() or {}
    updated = False

    if "username" in payload:
        new_username = payload["username"].strip()
        if not new_username:
            return jsonify({"error": "Username cannot be empty"}), 400

        # check existing username
        if User.query.filter_by(username=new_username).first():
            return jsonify({"error": "Username already taken"}), 400

        current_user.username = new_username
        updated = True

    if "password" in payload:
        pwd = payload["password"].strip()
        if len(pwd) < 6:
            return jsonify({"error": "Password too short"}), 400

        current_user.password_hash = generate_password_hash(pwd)
        updated = True

    if not updated:
        return jsonify({"error": "Nothing to update"}), 400

    db.session.commit()
    return jsonify({"message": "Profile updated"}), 200


# -------------------------------
# PATCH /users/<id>/role  → admin only
# -------------------------------
