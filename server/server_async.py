import asyncio
import logging
import sys
import json
from database.read import fetch_chat


# Default parameters
HOSTNAME = "localhost"  # ip: 127.0.0.1
PORT = 8888  # arbitrary high level port


class Server:

    def __init__(self, hostname: str = HOSTNAME, port: int = PORT, logging_level: str = logging.WARN):
        self.connected_clients = []  # List for now, might need to change data structure
        self.database = None  # Placeholder for database
        self.hostname = hostname
        self.port = port
        self.logger = logging.getLogger("Server_logger")
        self.logger.setLevel(logging_level)
        logging.basicConfig(stream=sys.stdout, level=logging_level)

    # Async def makes the function a 'coroutine'
    # basically a function that can be run using concurrency
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Coroutine which handles incoming client connections parallel
        :param reader: asyncio.StreamReader - wrapper for async reading to TCP sockets
        :param writer: asyncio.StreamWriter - wrapper for async writing to TCP sockets
        :return:
        """
        addr = writer.get_extra_info("peername")
        logging.info(f"Client {addr} connected.")
        self.connected_clients.append(addr)  # Add this client to list of currently connected clients
        data = await reader.read(100)  # to run coroutines you need to call them using the 'await' keyword
        message = data.decode()  # Decoding message from bytestream to utf-8 encoded text
        request = await self.parse_request(json.loads(message))
        logging.info(f"Received {message!r} from {addr!r}")
        # print(f"Send: {message!r}")

        # Need to use write with drain as it might be queued in a write buffer
        # if it cannot be sent immediately
        writer.write(data)
        await writer.drain()

        # print("Close the connection")
        writer.close()

    # Returns a callback
    async def parse_request(self, request: dict):
        """
        Coroutine which parses client requests.
        The requests will be in json format
        :param request: json format of request
        :return callback: action (future)
        """
        match request["code"]:
            case "READ":
                self.logger.debug(f"READ request from {request['from_other']}")
                return fetch_chat(request["from_other"])
            case "WRITE":
                self.logger.debug(f"WRITE request to {request['to']} : {request['payload']}")
            case "LOGIN":
                pass
            case "LOGOUT":
                pass
            case "REGISTER":
                pass

    async def main(self):
        """
        Entry point for server code
        :return:
        """
        # asyncio makes it easy to start tcp servers using start_server
        # It's already both IPv4 and IPv6
        server = await asyncio.start_server(self.handle_client, self.hostname, self.port)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        logging.info(f"Serving on {addrs}")

        async with server:
            await server.serve_forever()


