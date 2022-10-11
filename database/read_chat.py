from .database_connect import logging
from .config import (
    _select_private_window,
    _select_receiver_where_more_than_1,
    _select_group_window,
)

# from database_connect import db_connect, logging
# from config import _select_private_window, _select_receiver_where_more_than_1, _select_group_window


def private_window(conn, cursor, employee_id, receiver_id):
    cursor.execute(
        _select_private_window,
        (
            employee_id,
            receiver_id,
        ),
    )
    rows = cursor.fetchall()
    return rows


def group_window(conn, cursor, employee_id, receiver_ids):
    cursor.execute(_select_receiver_where_more_than_1)
    all_groups = cursor.fetchall()  # list of tuple [('1,2,3',), ('2,1,3,4',)]
    sorted_group_members = sorted(receiver_ids)  # List of ints - [1,2,3,4]

    # tuple_list could be for unit testing this function
    # tuple_list = [('9, 0, 1, 3',), ('4, 0, 2, 7',), ('3, 2',)]
    rows_of_messages = []
    employee_id = int(employee_id)
    if employee_id in sorted_group_members:  # If employee is a member of the group then fetch messages from the group
        for group in all_groups:
            sorted_group = sorted(list(map(str.strip, group[0].split(","))))
            sorted_group_of_int = list(
                map(int, sorted_group)
            )  # List of ints - [1,2,3,4]
            if sorted_group_members == sorted_group_of_int:  # [1,2,3,4] ==  [1,2,3,4]
                cursor.execute(_select_group_window, (group[0],))
                rows = cursor.fetchall()
                if rows not in rows_of_messages:
                    rows_of_messages.append(rows)
        # print("rows_of_messages - ", rows_of_messages)
        return rows_of_messages


def fetch_chat(conn, cursor, employee_id, receiver_id):
    receiver = list(map(int, receiver_id.split(",")))
    if len(receiver) > 1:
        logging.info("group window open")
        return group_window(conn, cursor, employee_id, receiver)
    else:
        logging.info("private window")
        return private_window(conn, cursor, employee_id, receiver[0])


# conn, cursor = db_connect("sqlite.db")
# if __name__ == '__main__':
#     fetch_chat(conn, cursor, 2, '3,2,4,1')
