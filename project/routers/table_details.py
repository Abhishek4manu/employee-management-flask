from flask import Blueprint, jsonify
from project.models.employee import Employee
from project.utils.token import token_required
from project.utils.admin import admin_required
from project import db
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.get("/dashboard")
@token_required
@admin_required
def get_dashboard(current_user):
    # Total employees
    total = db.session.query(func.count(Employee.id)).scalar()

    # Average salary
    avg_salary = db.session.query(func.avg(Employee.salary)).scalar()

    # Department counts
    dept_counts = (
        db.session.query(Employee.department, func.count(Employee.id))
        .group_by(Employee.department)
        .all()
    )

    dept_data = {dept: count for dept, count in dept_counts}

    return jsonify({
        "total_employees": total,
        "avg_salary": avg_salary,
        "department_counts": dept_data
    }), 200
