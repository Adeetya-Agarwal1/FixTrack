import sqlite3


DATABASE = "fixtrack.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)

    # Allows us to access columns by name
    # Example: machine["machine_name"]
    connection.row_factory = sqlite3.Row

    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Machines table
    cursor.execute("""
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

    # Spare Parts table
    cursor.execute("""
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

    # Maintenance Records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER NOT NULL,
            spare_part_id INTEGER,
            quantity INTEGER DEFAULT 0,
            maintenance_date TEXT NOT NULL,
            remarks TEXT,

            FOREIGN KEY (machine_id) REFERENCES machines(id),
            FOREIGN KEY (spare_part_id) REFERENCES spare_parts(id)
        )
    """)

    connection.commit()
    connection.close()

    print("FixTrack database created successfully.")


if __name__ == "__main__":
    create_tables()