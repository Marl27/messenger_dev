from database import create
from server import server_async
import asyncio
import logging
import dotenv
import os
dotenv.load_dotenv()
create.create_table()
HOSTNAME = os.getenv('HOSTNAME')
PORT = os.getenv('PORT')

print('HOSTNAME- ', HOSTNAME, 'PORT - ', PORT)

server = server_async.Server(hostname=HOSTNAME, port=PORT, logging_level=logging.DEBUG)
asyncio.run(server.main())


