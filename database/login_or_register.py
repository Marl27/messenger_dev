from .database_connect import logging
from .config import _login_query, _insert_register_employee

# from database_connect import db_connect, logging
# from config import _login_query, _insert_register_employee


def login(conn, cursor, user_name, password):
    # conn, cursor = db_connect()
    cursor.execute(_login_query, (user_name, password,))
    row = cursor.fetchone()
    if row is not None:
        employee_id, *other = row
        logging.info('Login Successful')
        return True, employee_id
    else:
        return False, None


# _insert_register_employee = """
#         INSERT INTO employees ( first_name, start_date, username, password, middle_name, last_name, leaving_date)
#         VALUES(?,?,?,?,?,?,?)
#         """


def register(conn, cursor, first_name, start_date, username, password, middle_name, last_name, leaving_date):
    # conn, cursor = db_connect()
    with conn:
        cursor.execute(_insert_register_employee, (first_name, start_date, username, password, middle_name, last_name,
                                                   leaving_date,))
    logging.info('Employee Registered')


# user_name = 'him.s'
# password = 'password'


# if __name__ == '__main__':
#     register('Big', '01/08/2022', 'big.person', 'password', 's', 'Person', '')
