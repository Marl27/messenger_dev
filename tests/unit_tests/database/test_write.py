import sys
import pytest
sys.path.append(".")
from database.write_chat import write_chat
from database.read_chat import fetch_chat
from tests.database_config import db_connect_for_testing

# TODO - More tests
expected_chats = {
    "1": [(1, '2', 0, None, 'user_1 sending to user_2', 0)],

}


@pytest.mark.parametrize("sender_id, receiver_id, message, is_broadcasted, group_name, is_stared, expected", [
                        # Happy Path
                        (1, '2', 'user_1 sending to user_2', False, None, False, expected_chats['1']),
])
def test_write_chat(db_connect_for_testing, sender_id, receiver_id, message,
                    is_broadcasted, group_name, is_stared, expected):
    conn, cursor = db_connect_for_testing
    with conn:
        cursor.execute('DELETE FROM messenger')
        write_chat(conn, cursor, sender_id, receiver_id, message, is_broadcasted, group_name, is_stared)
    results = fetch_chat(conn, cursor, sender_id, receiver_id)
    # print('**test_write_chat**')
    # print(results)
    # print(expected)
    if len(receiver_id) == 1:
        results_without_timestamp = [result[:6] for result in results]
    else:
        results_without_timestamp = [[x[:6] for x in result] for result in results]

    assert results_without_timestamp == expected
