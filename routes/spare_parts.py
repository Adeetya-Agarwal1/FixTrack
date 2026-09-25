from flask import Blueprint, render_template, request, redirect, url_for

from database import get_connection


spare_parts_bp = Blueprint(
    "spare_parts",
    __name__,
    url_prefix="/spare-parts"
)


@spare_parts_bp.route("/")
def spare_parts():

    connection = get_connection()

    parts = connection.execute(
        "SELECT * FROM spare_parts ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "spare_parts/index.html",
        parts=parts
    )


@spare_parts_bp.route("/add", methods=["GET", "POST"])
def add_spare_part():

    if request.method == "POST":

        part_code = request.form["part_code"]
        part_name = request.form["part_name"]
        category = request.form["category"]
        brand = request.form["brand"]
        specification = request.form["specification"]
        current_stock = request.form["current_stock"]
        reorder_level = request.form["reorder_level"]
        location = request.form["location"]

        connection = get_connection()

        connection.execute("""
            INSERT INTO spare_parts
            (
                part_code,
                part_name,
                category,
                brand,
                specification,
                current_stock,
                reorder_level,
                location
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            part_code,
            part_name,
            category,
            brand,
            specification,
            current_stock,
            reorder_level,
            location
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("spare_parts.spare_parts"))

    return render_template("spare_parts/add.html")


@spare_parts_bp.route("/edit/<int:part_id>", methods=["GET", "POST"])
def edit_spare_part(part_id):

    connection = get_connection()

    part = connection.execute(
        "SELECT * FROM spare_parts WHERE id = ?",
        (part_id,)
    ).fetchone()

    if request.method == "POST":

        part_code = request.form["part_code"]
        part_name = request.form["part_name"]
        category = request.form["category"]
        brand = request.form["brand"]
        specification = request.form["specification"]
        current_stock = request.form["current_stock"]
        reorder_level = request.form["reorder_level"]
        location = request.form["location"]

        connection.execute("""
            UPDATE spare_parts
            SET
                part_code = ?,
                part_name = ?,
                category = ?,
                brand = ?,
                specification = ?,
                current_stock = ?,
                reorder_level = ?,
                location = ?
            WHERE id = ?
        """, (
            part_code,
            part_name,
            category,
            brand,
            specification,
            current_stock,
            reorder_level,
            location,
            part_id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("spare_parts.spare_parts"))

    connection.close()

    return render_template(
        "spare_parts/edit.html",
        part=part
    )


@spare_parts_bp.route("/delete/<int:part_id>")
def delete_spare_part(part_id):

    connection = get_connection()

    connection.execute(
        "DELETE FROM spare_parts WHERE id = ?",
        (part_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("spare_parts.spare_parts"))