import sys
import pytest
sys.path.append(".")
from database.write_chat import write_chat
from tests.database_config import db_connect_for_testing


expected_chats = {
    "1": [(1, '2', 0, None, 'private message', 0),
          (2, '1', 0, None, 'Hi Char', 0),
          (1, '2', 0, None, 'Hi Him', 0)],

    "2": [(1, '2', 0, None, 'private message', 0),
          (2, '1', 0, None, 'Hi Char', 0),
          (1, '2', 0, None, 'Hi Him', 0)],

    "2,1,3": [[(1, '1,2,3', 0, 'group_1', 'anyone home?', 0),
               (2, '1,2,3', 0, 'group_1', 'anyone home?', 0)]],

    "2,1,3,4": [[(1, '1,2,3,4', 0, 'group_2', 'testing sort', 0), (2, '1,2,3,4', 0, 'group_2', 'testing sort 3', 0)],
                [(2, '2,1,3,4', 0, None, 'group chat, multiple receiver test', 0),
                 (2, '2,1,3,4', 0, None, 'multiple receiver test1', 0)]],
}

# TODO
#
# @pytest.mark.parametrize("employee_id, receiver_id, expected", [
#     # Happy Path
#     (1, '2', expected_chats['2']),
#     (2, '1', expected_chats['2']),
#     (1, '2,1,3', expected_chats['2,1,3']),
#     (2, '2,1,3,4', expected_chats['2,1,3,4']),
#     # Unhappy Path
#     # (1, 2, "AttributeError: 'int' object has no attribute 'split'")
# ])
# def test_fetch_chat(db_connect_for_testing, employee_id, receiver_id, expected):
#     conn, cursor = db_connect_for_testing
#     results = write_chat(conn, cursor, employee_id, receiver_id)
#     if len(receiver_id) == 1:
#         results_without_timestamp = [result[:6] for result in results]
#     else:
#         results_without_timestamp = [[x[:6] for x in result] for result in results]
#     assert expected == results_without_timestamp