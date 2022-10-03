from database import create
create.create_table()

from server import server_async
import asyncio
import logging

server = server_async.Server(logging_level=logging.INFO)
asyncio.run(server.main())
