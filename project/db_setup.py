import sqlite3

def create_connection():
    conn = sqlite3.connect("employees.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            department TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
