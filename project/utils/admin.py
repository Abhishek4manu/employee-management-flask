from functools import wraps
from flask import jsonify
from project.models.user import User

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):

        # token_required already passed current_user
        if current_user.role != "admin":
            return jsonify({"error": "Admin privilege required"}), 403

        return f(current_user, *args, **kwargs)
    return decorated
