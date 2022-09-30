from database_connect import db_connect


def private_window(receiver):
    conn = db_connect().cursor()
    conn.execute("SELECT * FROM messenger m WHERE receiver = ?", (receiver,))
    rows = conn.fetchall()
    return rows


def group_window():
    pass


def fetch_chat(user_id):
    user = list(map(int, user_id.split(',')))
    if len(user) > 1:
        print('group chat')
    else:
        print('private chat')
        print(user[0])
        private_window(user[0])



