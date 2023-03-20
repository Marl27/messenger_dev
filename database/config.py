# --------------------------------------------------------------------------
# read_chat.py
# --------------------------------------------------------------------------
# SELECT statements
_select_private_window = "SELECT * FROM messenger m WHERE sender IN (?,?) AND receiver IN (?,?)"
_select_group_window = "SELECT * FROM messenger m WHERE receiver = ?"
_select_receiver_where_more_than_1 = "SELECT receiver FROM messenger m WHERE LENGTH(receiver) > 1"
_select_all_chats = """
WITH CHAT_WITH_CTE AS(
SELECT e.first_name, m.sender, m.receiver, m.is_broadcasted, m.group_name, m.message, m.is_stared, m.created_at
, CASE WHEN LENGTH(m.group_name) > 0 THEN m.group_name
    ELSE (SELECT group_concat(e.first_name, ',') 
    FROM employees e
    WHERE ',' || m.receiver || ',' LIKE '%,' || e.employee_id || ',%')
    END AS CHAT_WITH
FROM messenger m
JOIN employees e on e.employee_id = m.sender  
WHERE sender = ? --UPDATE variable
ORDER BY m.created_at DESC
), GROUPED_BY_RECEIVERS AS(
SELECT * 
FROM CHAT_WITH_CTE
GROUP BY receiver 
) SELECT * 
FROM GROUPED_BY_RECEIVERS
ORDER BY  created_at DESC
"""

# --------------------------------------------------------------------------
# login_or_register.py
# --------------------------------------------------------------------------
# SELECT statements
_login_query = "SELECT employee_id FROM employees e WHERE username = ? AND password = ?"

# INSERT statements
_insert_register_employee = """ 
INSERT INTO employees (first_name, start_date, username, password, middle_name, last_name, leaving_date) 
VALUES(?,?,?,?,?,?,?)"""

# UPDATE statements

# --------------------------------------------------------------------------
# write_chat.py
# --------------------------------------------------------------------------
# INSERT statements for private and group chat
_insert_private_chat = """
INSERT INTO messenger (sender, receiver, message, is_broadcasted, group_name, is_stared) 
VALUES(?,?,?,?,?,?)"""

#
# --------------------------------------------------------------------------
# create.py
# --------------------------------------------------------------------------

_create_table_statement = """
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
            is_stared BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """