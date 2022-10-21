from .config import _create_table_statement


def create_table(conn, cursor):
    try:
        cursor.executescript(_create_table_statement)
    except conn.DatabaseError:
        conn.rollback()
        raise RuntimeError("Uh oh, an error occurred while Creating tables...")
