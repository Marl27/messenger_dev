from .database_connect import db_connect


def create_table():
    conn, cursor = db_connect()
    try:
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS employees (
          employee_id INTEGER PRIMARY KEY AUTOINCREMENT ,
          first_name VARCHAR,
          middle_name VARCHAR,
          last_name VARCHAR,
          username VARCHAR,
          password VARCHAR NOT NULL,
          start_date DATETIME,
          leaving_date DATETIME,
          created_at timestamp DEFAULT CURRENT_TIMESTAMP,
          updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
          UNIQUE (first_name, username, start_date)
        );  

        CREATE TABLE IF NOT EXISTS messenger(
            sender int NOT NULL,
            receiver VARCHAR NOT NULL,
            is_broadcasted BOOLEAN,
            group_name varchar,
            message TEXT NOT NULL,
            stared BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    except conn.DatabaseError:
        conn.rollback()
        raise RuntimeError("Uh oh, an error occurred while Creating tables...")
