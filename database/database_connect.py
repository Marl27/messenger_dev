import sqlite3
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def db_connect(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print("Opened database successfully")
    return conn, cursor
