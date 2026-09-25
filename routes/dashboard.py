from flask import Blueprint, render_template

from database import get_connection


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def dashboard():

    connection = get_connection()


    total_machines = connection.execute(
        "SELECT COUNT(*) FROM machines"
    ).fetchone()[0]


    total_spare_parts = connection.execute(
        "SELECT COUNT(*) FROM spare_parts"
    ).fetchone()[0]


    low_stock_items = connection.execute("""
        SELECT COUNT(*)
        FROM spare_parts
        WHERE current_stock <= reorder_level
    """).fetchone()[0]


    total_maintenance = connection.execute(
        "SELECT COUNT(*) FROM maintenance"
    ).fetchone()[0]


    recent_records = connection.execute("""
        SELECT
            maintenance.quantity,
            maintenance.maintenance_date,
            maintenance.remarks,

            machines.machine_number,
            machines.machine_name,

            spare_parts.part_name,
            spare_parts.brand,
            spare_parts.specification

        FROM maintenance

        JOIN machines
            ON maintenance.machine_id = machines.id

        LEFT JOIN spare_parts
            ON maintenance.spare_part_id = spare_parts.id

        ORDER BY maintenance.id DESC

        LIMIT 5
    """).fetchall()


    connection.close()


    return render_template(
        "dashboard/index.html",

        total_machines=total_machines,
        total_spare_parts=total_spare_parts,
        low_stock_items=low_stock_items,
        total_maintenance=total_maintenance,

        recent_records=recent_records
    )