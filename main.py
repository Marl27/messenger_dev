from database import database_connect
from database import create
from server import server_async
import asyncio
import logging
import dotenv
import os
dotenv.load_dotenv()
HOSTNAME = os.getenv('HOSTNAME')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB_NAME')

conn, cursor = database_connect.db_connect(DB_NAME)
print('DB_NAME - ', DB_NAME)
create.create_table(conn, cursor)

print('HOSTNAME- ', HOSTNAME, 'PORT - ', PORT)

server = server_async.Server(hostname=HOSTNAME, port=PORT, conn=conn, cursor=cursor, logging_level=logging.DEBUG)
asyncio.run(server.main())


