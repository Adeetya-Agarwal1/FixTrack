from flask import Blueprint, render_template, request, redirect, url_for

from database import get_connection


maintenance_bp = Blueprint(
    "maintenance",
    __name__,
    url_prefix="/maintenance"
)


@maintenance_bp.route("/")
def maintenance():

    connection = get_connection()

    records = connection.execute("""
        SELECT
            maintenance.id,
            maintenance.quantity,
            maintenance.maintenance_date,
            maintenance.remarks,

            machines.machine_number,
            machines.machine_name,

            spare_parts.part_code,
            spare_parts.part_name,
            spare_parts.brand,
            spare_parts.specification

        FROM maintenance

        JOIN machines
            ON maintenance.machine_id = machines.id

        LEFT JOIN spare_parts
            ON maintenance.spare_part_id = spare_parts.id

        ORDER BY maintenance.id DESC
    """).fetchall()

    connection.close()

    return render_template(
        "maintenance/index.html",
        records=records
    )


@maintenance_bp.route("/add", methods=["GET", "POST"])
def add_maintenance():

    connection = get_connection()

    machines = connection.execute(
        "SELECT * FROM machines ORDER BY machine_number"
    ).fetchall()

    spare_parts = connection.execute(
        "SELECT * FROM spare_parts ORDER BY part_name"
    ).fetchall()

    if request.method == "POST":

        machine_id = request.form["machine_id"]

        spare_part_id = request.form.get("spare_part_id")

        quantity = int(request.form.get("quantity", 0))

        maintenance_date = request.form["maintenance_date"]

        remarks = request.form["remarks"]


        # If no spare part is selected
        if spare_part_id == "":
            spare_part_id = None
            quantity = 0


        # Check available stock
        if spare_part_id:

            part = connection.execute(
                "SELECT * FROM spare_parts WHERE id = ?",
                (spare_part_id,)
            ).fetchone()

            if quantity > part["current_stock"]:

                error = (
                    f"Not enough stock available. "
                    f"Only {part['current_stock']} unit(s) of "
                    f"{part['part_name']} are currently available."
                )

                form_data = {
                    "machine_id": machine_id,
                    "spare_part_id": spare_part_id,
                    "quantity": quantity,
                    "maintenance_date": maintenance_date,
                    "remarks": remarks
                }

                connection.close()

                return render_template(
                    "maintenance/add.html",
                    machines=machines,
                    spare_parts=spare_parts,
                    error=error,
                    form_data=form_data
                )


        # Save maintenance record
        connection.execute("""
            INSERT INTO maintenance
            (
                machine_id,
                spare_part_id,
                quantity,
                maintenance_date,
                remarks
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            machine_id,
            spare_part_id,
            quantity,
            maintenance_date,
            remarks
        ))


        # Deduct spare part stock
        if spare_part_id and quantity > 0:

            connection.execute("""
                UPDATE spare_parts
                SET current_stock = current_stock - ?
                WHERE id = ?
            """, (
                quantity,
                spare_part_id
            ))


        connection.commit()
        connection.close()

        return redirect(url_for("maintenance.maintenance"))


    connection.close()

    return render_template(
        "maintenance/add.html",
        machines=machines,
        spare_parts=spare_parts
    )