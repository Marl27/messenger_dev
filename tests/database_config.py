import sqlite3
from pytest import fixture
import sys
sys.path.append(".")
from database.config import _create_table_statement

insert_statements = {
    "insert_1": """INSERT INTO employees
    ( first_name, start_date, username, password, middle_name, last_name, leaving_date)
    VALUES( 'char', 's', 'Rut', 'char.rut', 'password', '01/01/2022', '');""",

    "insert_2": """INSERT INTO employees
    ( first_name, middle_name, last_name, username, password, start_date, leaving_date)
    VALUES( 'him', 's', 'sah', 'him.s', 'password', '30/10/2022', '');""",

    "insert_3": """INSERT INTO employees
    ( first_name, middle_name, last_name, username, password, start_date, leaving_date)
    VALUES( 'random', 's', 'person', 'random.p', 'password', '28/10/2022', '');""",

    "insert_4": """INSERT INTO employees
    ( first_name, middle_name, last_name, username, password, start_date)
    VALUES( 'big', 's', 'bird', 'big.b', 'password', '28/10/2022');""",

    "insert_5_1": """INSERT INTO messenger 
    (sender, receiver, is_broadcasted, message, is_stared) 
    VALUES(1, '2', 0, 'private message', 0);""",

    "insert_5_2": """INSERT INTO messenger 
    (sender, receiver, is_broadcasted, message, is_stared) 
    VALUES(2, '1', 0, 'Hi Char', 0);""",

    "insert_5_3": """INSERT INTO messenger 
    (sender, receiver, is_broadcasted, message, is_stared) 
    VALUES(1, '2', 0, 'Hi Him', 0);""",

    "insert_6_1": """INSERT INTO messenger 
    (sender, receiver, is_broadcasted, group_name, message, is_stared) 
    VALUES(1, '1,2,3', 0, 'group_1', 'anyone home?', 0);""",
    "insert_6_2": """INSERT INTO messenger 
    (sender, receiver, is_broadcasted, group_name, message, is_stared) 
    VALUES(2, '1,2,3', 0, 'group_1', 'anyone home?', 0);""",

    "insert_7_1": """INSERT INTO messenger 
    (sender, receiver, is_broadcasted, group_name, message, is_stared) 
    VALUES(1, '1,2,3,4', 0, 'group_2', 'testing sort', 0);""",

    "insert_7_2": """INSERT INTO messenger
    (sender, receiver, is_broadcasted, group_name, message, is_stared)
    VALUES(2, '1,2,3,4', 0, 'group_2', 'testing sort 3', 0);""",

    "insert_7_3": """INSERT INTO messenger 
    (sender, receiver, is_broadcasted, message, is_stared) 
    VALUES(2, '2,1,3,4', 0, 'group chat, multiple receiver test', 0);""",

    "insert_7_4": """INSERT INTO messenger
    (sender, receiver, is_broadcasted, message, is_stared)
    VALUES(2, '2,1,3,4', 0, 'multiple receiver test1', 0);""",



    #
    # "insert_11": """INSERT INTO messenger
    # (sender, receiver, is_broadcasted, message, is_stared)
    # VALUES(2, '2,1,3,4', 0, 'group chat', 0);""",
    #
    # "insert_12": """INSERT INTO messenger
    # (sender, receiver, is_broadcasted, message, is_stared)
    # VALUES(2, '2,1,3,4', 0, 'group chat', 0);""",




}


@fixture(autouse=True)
def db_connect_for_testing():
    """create a database connection to a database that resides
    in the memory
    """
    conn = sqlite3.connect(":memory:")
    with conn:
        cursor = conn.cursor()
        cursor.executescript(_create_table_statement)
        for i in insert_statements:
            cursor.execute(insert_statements[i])

        # cursor.execute("SELECT * FROM employees")
        # test = cursor.fetchall()
        #
        cursor.execute("SELECT * FROM messenger WHERE sender = 1 AND receiver = '2'")
        test1 = cursor.fetchall()
        # print(test, '\n')
        print(test1)

    return conn, cursor
