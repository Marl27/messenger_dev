import sqlite3
import pytest

# from .database.database_connect import db_connect
import sys

sys.path.append(".")
import os

print("Current working directory ", os.getcwd())
from database.create import create_table


def db_connect():
    """create a database connection to a database that resides
    in the memory
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    return conn, cursor


# conn, cursor = db_connect()


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_create_table():
    test = create_table()
    assert True
