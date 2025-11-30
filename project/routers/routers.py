from flask import Blueprint, request, jsonify, render_template
from project import db
from project.models.employee import Employee
from project.utils.token import token_required
from project.utils.admin import admin_required
from project.schemas.employee_schema import EmployeeCreateSchema, EmployeeUpdateSchema
from project.utils.logger import log_action
from datetime import datetime
employees_bp = Blueprint(
    "employees",
    __name__,
    url_prefix="/employees",
    template_folder="templates"
)

# ----------------------------------------
# Helper: Salary Redaction for non-admins
# ----------------------------------------
def redact_salary(emp_dict, current_user):
    if current_user.role != "admin":
        emp_dict.pop("salary", None)
    return emp_dict


# ----------------------------------------
# GET ALL (search + filter + sort + pagination)
# ----------------------------------------
@employees_bp.get("/")
def home():
    return jsonify({"message": "Employee API is running"}), 200

@employees_bp.get("")
@token_required
def get_employees(current_user):
    query = Employee.query

    # --- Search ---
    search = request.args.get("search")
    if search:
        like = f"%{search}%"
        query = query.filter(
            (Employee.name.ilike(like)) |
            (Employee.department.ilike(like)) |
            (Employee.email.ilike(like))
        )

    # --- Filters ---
    dept = request.args.get("department")
    if dept:
        query = query.filter(Employee.department.ilike(f"%{dept}%"))

    min_age = request.args.get("min_age", type=int)
    if min_age is not None:
        query = query.filter(Employee.age >= min_age)

    max_age = request.args.get("max_age", type=int)
    if max_age is not None:
        query = query.filter(Employee.age <= max_age)

    min_salary = request.args.get("min_salary", type=float)
    if min_salary is not None:
        query = query.filter(Employee.salary >= min_salary)

    max_salary = request.args.get("max_salary", type=float)
    if max_salary is not None:
        query = query.filter(Employee.salary <= max_salary)

    # --- Sorting ---
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    if hasattr(Employee, sort_by):
        col = getattr(Employee, sort_by)
        if order == "desc":
            col = col.desc()
        query = query.order_by(col)

    # --- Pagination ---
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    items = query.paginate(page=page, per_page=limit, error_out=False)

    data = [redact_salary(emp.to_dict(), current_user) for emp in items.items]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": items.total,
        "pages": items.pages,
        "data": data
    }), 200


# ----------------------------------------
# GET BY ID
# ----------------------------------------
@employees_bp.get("/<int:emp_id>")
@token_required
def get_employee(current_user, emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    data = redact_salary(emp.to_dict(), current_user)
    return jsonify(data), 200


# ----------------------------------------
# CREATE EMPLOYEE (Admin only)
# ----------------------------------------
@employees_bp.post("")
@token_required
@admin_required
def create_employee(current_user):
    schema = EmployeeCreateSchema()

    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    emp = Employee(
        name=data["name"],
        age=data["age"],
        email=data["email"],
        department=data["department"],
        salary=data["salary"]
    )

    db.session.add(emp)
    db.session.commit()
    log_action(current_user.id, "Employee data created",datetime.utcnow(),emp.id)

    return jsonify(emp.to_dict()), 201


# ----------------------------------------
# PUT (full update)
# ----------------------------------------
@employees_bp.put("/<int:emp_id>")
@token_required
@admin_required
def update_employee(current_user, emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    schema = EmployeeCreateSchema()
    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    emp.name = data["name"]
    emp.age = data["age"]
    emp.email = data["email"]
    emp.department = data["department"]
    emp.salary = data["salary"]

    db.session.commit()
    log_action(current_user.id, "Employee data updated",datetime.utcnow(),emp.id)
    return jsonify(emp.to_dict()), 200


# ----------------------------------------
# PATCH (partial update)
# ----------------------------------------
@employees_bp.patch("/<int:emp_id>")
@token_required
@admin_required
def patch_employee(current_user, emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    schema = EmployeeUpdateSchema()
    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    for key, value in data.items():
        setattr(emp, key, value)

    db.session.commit()
    log_action(current_user.id, "Employee data updated",datetime.utcnow(),emp.id)
    return jsonify(emp.to_dict()), 200


# ----------------------------------------
# DELETE EMPLOYEE
# ----------------------------------------
@employees_bp.delete("/<int:emp_id>")
@token_required
@admin_required
def delete_employee(current_user, emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(emp)
    db.session.commit()
    log_action(current_user.id, "Employee data deleted",datetime.utcnow(),emp.id)

    return jsonify({"message": "Employee deleted"}), 200


# ----------------------------------------
# HTML VIEW (optional)
# ----------------------------------------
@employees_bp.get("/")
def home():
    return render_template("employee.html")
