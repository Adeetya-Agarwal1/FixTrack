from flask import (Flask, session, redirect, url_for, request)
from database import create_tables

from routes.dashboard import dashboard_bp
from routes.machines import machines_bp
from routes.spare_parts import spare_parts_bp
from routes.maintenance import maintenance_bp
from routes.auth import auth_bp
from routes.reports import reports_bp

app = Flask(__name__)
app.secret_key = "fixtrack-secret-key-change-later"

app.register_blueprint(dashboard_bp)
app.register_blueprint(machines_bp)
app.register_blueprint(spare_parts_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)

@app.before_request
def require_login():

    allowed_endpoints = [
        "auth.login",
        "static"
    ]

    if request.endpoint in allowed_endpoints:
        return

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

create_tables()


if __name__ == "__main__":
    app.run(debug=True)