from database import create
from server import server_async
import asyncio
import logging

create.create_table()

server = server_async.Server(logging_level=logging.DEBUG)
asyncio.run(server.main())
