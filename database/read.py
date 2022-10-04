from .database_connect import db_connect
#from database_connect import db_connect

import dotenv
import os
dotenv.load_dotenv()

print('SQL QUERY - ', os.getenv("private_window_query"))

def private_window(receiver):
    conn = db_connect().cursor()
    conn_man = db_connect().cursor()
    conn.execute("SELECT * FROM messenger m WHERE receiver = ?", (receiver,))
    rows = conn.fetchall()
    print(type(rows))
    return rows


def group_window(receivers):
    conn = db_connect().cursor()
    conn.execute("SELECT receiver FROM messenger m")
    all_groups = conn.fetchall()
    group_members = sorted(receivers)

    # tuplelist could be for unit testing this function
    # tuplelist = [('9, 0, 1, 3',), ('4, 0, 2, 7',), ('3, 2',)]

    for group in all_groups:
        sorted_group = sorted(list(map(str.strip, group[0].split(','))))
        sorted_group_int = list(map(int, sorted_group))
        if group_members == sorted_group_int:
            group_members_str = ','.join(list(map(str, group_members)))
            conn.execute("SELECT * FROM messenger m WHERE receiver = ?", (group_members_str,))
            rows = conn.fetchall()
            print(rows)


def fetch_chat(user_id):
    user = list(map(int, user_id.split(',')))
    if len(user) > 1:
        print('group chat')
        group_window(user)
    else:
        return private_window(user[0])



# if __name__ == '__main__':
#     fetch_chat('3,2,4')
