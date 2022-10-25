from database.login_or_register import login


class User:

    def __init__(self, conn, cursor, username, password):
        self.conn = conn
        self.cursor = cursor
        self.username = username
        self.password = password

    def login(self):
        return login(self.conn, self.cursor, self.username, self.password)  # True, employee_id