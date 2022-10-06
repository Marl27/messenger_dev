import sqlite3
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def db_connect():
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    print("Opened database successfully")
    return conn, cursor
