from .database_connect import db_connect, logging
from .config import _select_private_window, _select_receiver_from_messenger, _select_group_window

# from database_connect import db_connect, logging
# from config import _select_private_window, _select_receiver_from_messenger, _select_group_window


def private_window(receiver):
    conn = db_connect().cursor()
    conn.execute(_select_private_window, (receiver,))
    rows = conn.fetchall()
    print(rows)
    return rows


def group_window(receivers):
    conn = db_connect().cursor()
    conn.execute(_select_receiver_from_messenger)
    all_groups = conn.fetchall()
    group_members = sorted(receivers)

    # tuple_list could be for unit testing this function
    # tuple_list = [('9, 0, 1, 3',), ('4, 0, 2, 7',), ('3, 2',)]

    for group in all_groups:
        sorted_group = sorted(list(map(str.strip, group[0].split(','))))
        sorted_group_int = list(map(int, sorted_group))
        if group_members == sorted_group_int:
            group_members_str = ','.join(list(map(str, group_members)))
            conn.execute(_select_group_window, (group_members_str,))
            rows = conn.fetchall()
            print(rows)
            return rows


def fetch_chat(user_id):
    user = list(map(int, user_id.split(',')))
    if len(user) > 1:
        logging.info('group window open')
        return group_window(user)
    else:
        logging.info('private window')
        return private_window(user[0])


# if __name__ == '__main__':
#     fetch_chat('2,4,3')
