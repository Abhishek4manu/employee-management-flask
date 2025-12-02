from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = None

def create_app():
    app = Flask(__name__)

    # PRIORITY: use PostgreSQL if DATABASE_URL exists
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Render gives DATABASE_URL starting with "postgres://"
        # SQLAlchemy requires "postgresql://"
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        # fallback - local sqlite
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        DB_PATH = os.path.join(BASE_DIR, "..", "employees.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

    db.init_app(app)

    # import models so Alembic can detect them
    from project.models.employee import Employee
    from project.models.user import User

    global migrate
    migrate = Migrate(app, db)

    # register routes
    from project.routers.routers import employees_bp
    app.register_blueprint(employees_bp, url_prefix="/employees")

    from project.routers.auth_routers import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from project.routers.user_routers import user_bp
    app.register_blueprint(user_bp, url_prefix="/user")

    from project.routers.admin_routers import log_bp
    app.register_blueprint(log_bp, url_prefix="/admin")

    from project.routers.table_details import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix="/analysis")

    # only for first deploy — auto create tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()
