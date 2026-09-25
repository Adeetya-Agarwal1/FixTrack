from flask import Flask

from database import create_tables
from routes.dashboard import dashboard_bp
from routes.machines import machines_bp
from routes.spare_parts import spare_parts_bp
from routes.maintenance import maintenance_bp

app = Flask(__name__)


# Register routes
app.register_blueprint(dashboard_bp)
app.register_blueprint(machines_bp)
app.register_blueprint(spare_parts_bp)
app.register_blueprint(maintenance_bp)

# Create database tables if they don't already exist
create_tables()


if __name__ == "__main__":
    app.run(debug=True)