from flask import Blueprint, render_template

from database import get_connection


reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports")
def reports():

    connection = get_connection()

    consumption_report = connection.execute(
        """
        SELECT
            spare_parts.part_code,
            spare_parts.part_name,
            spare_parts.brand,
            spare_parts.specification,
            SUM(maintenance.quantity) AS total_used,
            COUNT(maintenance.id) AS maintenance_count
        FROM maintenance
        JOIN spare_parts
            ON maintenance.spare_part_id = spare_parts.id
        WHERE maintenance.spare_part_id IS NOT NULL
        GROUP BY spare_parts.id
        ORDER BY total_used DESC
        """
    ).fetchall()

    total_consumed = connection.execute(
        """
        SELECT COALESCE(SUM(quantity), 0) AS total
        FROM maintenance
        WHERE spare_part_id IS NOT NULL
        """
    ).fetchone()["total"]

    total_parts_used = connection.execute(
        """
        SELECT COUNT(DISTINCT spare_part_id) AS total
        FROM maintenance
        WHERE spare_part_id IS NOT NULL
        """
    ).fetchone()["total"]

    total_records = connection.execute(
        """
        SELECT COUNT(*) AS total
        FROM maintenance
        WHERE spare_part_id IS NOT NULL
        """
    ).fetchone()["total"]

    connection.close()

    return render_template(
        "reports/index.html",
        consumption_report=consumption_report,
        total_consumed=total_consumed,
        total_parts_used=total_parts_used,
        total_records=total_records
    )