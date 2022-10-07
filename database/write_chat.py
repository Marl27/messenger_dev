from .database_connect import db_connect, logging
from .config import _insert_private_chat

# from database_connect import db_connect, logging
# from config import _insert_private_chat


def write_private_chat(sender_id, receiver_id, message, is_broadcasted=False, group_name=None, is_stared=False):
    conn, cursor = db_connect()
    with conn:
        cursor.execute(_insert_private_chat, (sender_id, receiver_id, message, is_broadcasted, group_name, is_stared,))
    logging.info('Private Chat Written')
    return True


def write_group_chat(sender_id, receiver_id, message, is_broadcasted=False, group_name=None, is_stared=False):
    if str(sender_id) not in receiver_id:
        receiver_id = str(sender_id)+','+receiver_id
    conn, cursor = db_connect()
    with conn:
        cursor.execute(_insert_private_chat, (sender_id, receiver_id, message, is_broadcasted, group_name, is_stared,))
    logging.info('Group Chat Written')
    return True


def write_chat(sender_id, receiver_id, message, is_broadcasted=False, group_name=None, is_stared=False):
    receiver = list(map(int, receiver_id.split(',')))
    if len(receiver) > 1:
        logging.info('Writing Group Chat')
        return write_group_chat(sender_id, receiver_id, message, is_broadcasted, group_name, is_stared)
    else:
        logging.info('Writing Private Chat')
        return write_private_chat(sender_id, receiver[0], message, is_broadcasted, group_name, is_stared)

#
# if __name__ == "__main__":
#     write_chat(2, '2,1,3,4', 'group chat, multiple reciever test1', is_broadcasted=False, group_name=None, is_stared=False)