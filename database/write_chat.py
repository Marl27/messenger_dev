# from .database_connect import db_connect, logging
# from .config import _insert_register_employee

from database_connect import db_connect, logging
from config import _insert_register_employee


def write_private_chat(sender_id, receiver_id, message, is_broadcasted=False, group_name=None, is_stared=False):
    # conn, cursor = db_connect()
    # with conn:
    #     cursor.execute(_insert_register_employee, ())
    # logging.info('Employee Registered')
    print('write_private_chat')
    print(sender_id, receiver_id, message, is_broadcasted, group_name, is_stared)


def write_group_chat(sender_id, receiver_id, message, is_broadcasted=False, group_name=None, is_stared=False):
    # conn, cursor = db_connect()
    # with conn:
    #     cursor.execute(_insert_register_employee, ())
    # logging.info('Employee Registered')
    print('write_group_chat')
    print(sender_id, receiver_id, message, is_broadcasted, group_name, is_stared)


def write_chat(sender_id, receiver_id, message, is_broadcasted=False, group_name=None, is_stared=False):
    receiver = list(map(int, receiver_id.split(',')))
    if len(receiver) > 1:
        logging.info('writing group chat')
        return write_group_chat(sender_id, receiver, message, is_broadcasted, group_name, is_stared)
    else:
        logging.info('writing private chat')
        return write_private_chat(sender_id, receiver[0], message, is_broadcasted, group_name, is_stared)


if __name__ == "__main__":
    write_chat(2, '1', 'Hi Charlie', '', None, False)