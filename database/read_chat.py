from .database_connect import db_connect, logging
from .config import _select_private_window, _select_receiver_from_messenger, _select_group_window

# from database_connect import db_connect, logging
# from config import _select_private_window, _select_receiver_from_messenger, _select_group_window


def private_window(employee_id, receiver_id):
    conn, cursor = db_connect()
    cursor.execute(_select_private_window, (employee_id, receiver_id,))
    rows = cursor.fetchall()
    return rows


def group_window(employee_id, receiver_ids):
    conn, cursor = db_connect()
    cursor.execute(_select_receiver_from_messenger)
    all_groups = cursor.fetchall()
    group_members = sorted(receiver_ids)

    # tuple_list could be for unit testing this function
    # tuple_list = [('9, 0, 1, 3',), ('4, 0, 2, 7',), ('3, 2',)]

    if employee_id in group_members:  # If employee is a member of the group then fetch messages from the group
        for group in all_groups:
            sorted_group = sorted(list(map(str.strip, group[0].split(','))))
            sorted_group_int = list(map(int, sorted_group))
            if group_members == sorted_group_int:
                group_members_str = ','.join(list(map(str, group_members)))
                cursor.execute(_select_group_window, (group_members_str,))
                rows = cursor.fetchall()
                return rows


def fetch_chat(employee_id, receiver_id):
    receiver = list(map(int, receiver_id.split(',')))
    if len(receiver) > 1:
        logging.info('group window open')
        return group_window(employee_id, receiver)
    else:
        logging.info('private window')
        return private_window(employee_id, receiver[0])


# if __name__ == '__main__':
#     fetch_chat(1, '2,3,4,1')
