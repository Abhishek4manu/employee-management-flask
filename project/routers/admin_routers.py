from flask import Blueprint, jsonify
from project.models.activity_log import ActivityLog
from project.utils.token import token_required

log_bp = Blueprint("log_bp", __name__)


@log_bp.get("/logs")
@token_required
def get_logs(current_user):

    if current_user.role != "admin":
        return jsonify({"error": "Admin access required"}), 403

    logs = ActivityLog.query.order_by(ActivityLog.id.desc()).all()

    data = [
        {
            "id": l.id,
            "user_id": l.user_id,
            "action": l.action,
            "target_id": l.target_id,
            "timestamp": l.timestamp.isoformat()
        }
        for l in logs
    ]

    return jsonify(data), 200
