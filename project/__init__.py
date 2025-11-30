from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = None

def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "..", "employees.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    # Import all models so Alembic can detect them
    from project.models.employee import Employee
    from project.models.user import User

    global migrate
    migrate = Migrate(app, db)

    # Import and register blueprints
    from project.routers.routers import employees_bp
    app.register_blueprint(employees_bp, url_prefix="/employees")

    from project.routers.auth_routers import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from project.routers.user_routers import user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    from project.routers.admin_routers import log_bp
    app.register_blueprint(log_bp, url_prefix="/admin")

    from project.routers.table_details import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix="/anal")

    return app

app = create_app()