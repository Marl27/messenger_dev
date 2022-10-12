import sqlite3
# import pytest
from pytest import fixture
import sys
sys.path.append(".")
from database.create import create_table


@fixture()
def db_connect():
    """create a database connection to a database that resides
    in the memory
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    return conn, cursor




# @pytest.mark.parametrize("connection,cur, expected", [
#                         ("", 8),
#                         ("2+4", 6),
#                         ("6*9", 42)
# ])
def test_create_table(db_connect):
    #print(*db_connect)
    conn, cursor = db_connect
    create_table(conn, cursor)

    _sqlite_master = """
    SELECT tbl_name FROM sqlite_master 
    WHERE type = 'table';
    """
    cursor.execute(_sqlite_master)
    test = cursor.fetchall()
    print("****test_create_table***", test)
    # [('employees',), ('messenger',)]
    # [('employees',), ('sqlite_sequence',), ('messenger',)]
    assert all([('employees',) in test] and [('messenger',) in test])
    #assert False

# def create_tables():
