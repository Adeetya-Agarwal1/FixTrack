import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "fixtrack.db"


def get_connection():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_number TEXT UNIQUE NOT NULL,
            machine_name TEXT NOT NULL,
            department TEXT,
            manufacturer TEXT,
            model TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS spare_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_code TEXT UNIQUE NOT NULL,
            part_name TEXT NOT NULL,
            category TEXT,
            brand TEXT,
            specification TEXT,
            current_stock INTEGER DEFAULT 0,
            reorder_level INTEGER DEFAULT 5,
            location TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER NOT NULL,
            spare_part_id INTEGER,
            quantity INTEGER DEFAULT 0,
            maintenance_date TEXT NOT NULL,
            remarks TEXT,

            FOREIGN KEY (machine_id)
                REFERENCES machines(id)
                ON DELETE CASCADE,

            FOREIGN KEY (spare_part_id)
                REFERENCES spare_parts(id)
                ON DELETE SET NULL
        )
    """)
    
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    existing_user = connection.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if existing_user is None:

        connection.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (
                "admin",
                generate_password_hash("admin123")
            )
        )

    connection.commit()
    connection.close()