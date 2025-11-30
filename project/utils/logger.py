from project import db
from project.models.activity_log import ActivityLog


def log_action(user_id, action,timestamp,target_id=None):
    log = ActivityLog(
        user_id=user_id,
        action=action,
        target_id=target_id,
        timestamp=timestamp
    )
    db.session.add(log)
    db.session.commit()
