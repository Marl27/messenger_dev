# --------------------------------------------------------------------------
# read_chat.py
# --------------------------------------------------------------------------
# SELECT statements
_select_private_window = "SELECT * FROM messenger m WHERE sender = ? AND receiver = ?"
_select_group_window = "SELECT * FROM messenger m WHERE receiver = ?"
_select_receiver_from_messenger = "SELECT receiver FROM messenger m"


# --------------------------------------------------------------------------
# login_or_register.py
# --------------------------------------------------------------------------
# SELECT statements
_login_query = "SELECT employee_id FROM employees e WHERE username = ? AND password = ?"

# INSERT statements
_insert_register_employee = """
        INSERT INTO employees ( first_name, start_date, username, password, middle_name, last_name, leaving_date)
        VALUES(?,?,?,?,?,?,?)
        """

# UPDATE statements

# --------------------------------------------------------------------------
# write_chat.py
# --------------------------------------------------------------------------
# INSERT statements for private and group chat
_insert_private_chat = """
        INSERT INTO messenger (sender, receiver, message, is_broadcasted, group_name, is_stared) 
        VALUES(?,?,?,?,?,?)
        """
#
