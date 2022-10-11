from database.login_or_register import register, login

# from main import conn, cursor


class Employee:
    def __init__(
        self,
        conn,
        cursor,
        first_name,
        start_date,
        username,
        password,
        middle_name=None,
        last_name=None,
        leaving_date=None,
    ):
        self.conn = conn
        self.cursor = cursor
        self.first_name = first_name
        self.start_date = start_date
        self.username = username
        self.password = password
        self.middle_name = middle_name
        self.last_name = last_name
        self.leaving_date = leaving_date

    def register_employee(self):
        success = register(
            self.conn,
            self.cursor,
            self.first_name,
            self.start_date,
            self.username,
            self.password,
            self.middle_name,
            self.last_name,
            self.leaving_date,
        )
        if success:
            return True
        else:
            return False

    def login(self):
        return login(
            self.conn, self.cursor, self.username, self.password
        )  # True, employee_id
