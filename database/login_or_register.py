from .database_connect import db_connect
from .config import _login_query

# from database_connect import db_connect
# from config import _login_query

# user_name = 'him.s'
# password = 'password'


def login(user_name, password):
    conn = db_connect().cursor()
    conn.execute(_login_query, (user_name, password,))
    row = conn.fetchone()
    #print(rows)
    if row is not None:
        employee_id, *other = row
        return True, employee_id
    else:
        return False


# if __name__ == '__main__':
#     login(user_name, password)
