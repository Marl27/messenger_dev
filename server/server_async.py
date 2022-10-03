import asyncio
import logging
import sys
import json
from database.read import fetch_chat
from server import protocol

# Default parameters
HOSTNAME = "localhost"  # Should bind on all interfaces
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
        # Need to make sure message isn't truncated (1024 bytes max) and then we can't deserialise it

        data = await reader.read()  # to run coroutines you need to call them using the 'await' keyword
        message = data.decode()  # Decoding message from bytestream to utf-8 encoded text

        # this is generic, so to decide what kind of data will be returned from db
        # we need additional info i.e. what the "code" value is, but that's
        # the whole purpose of parse_request...
        request_type, db_response = await self.parse_request(json.loads(message))
        logging.info(f"Received {message!r} from {addr!r}")

        response = await protocol.Protocol.build_response(request_type, db_response)
        logging.info(f"Response message: {response}")
        # Need to use write with drain as it might be queued in a write buffer
        # if it cannot be sent immediately
        writer.write(bytes(json.dumps(response), encoding="utf-8"))
        await writer.drain()
        writer.write_eof()
        await writer.drain()

        # This method closes the stream AND the underlying socket
        writer.close()

    # Returns a callback
    async def parse_request(self, request: dict):
        """
        Coroutine which parses client requests.
        The requests will be in json format
        NOTE this will need to be expanded to handle multiple requests in the one json file
        :param request: json format of request
        :return (Protocol type Enum, [database response]): Returns a tuple with the function code and relevant data from database
        """
        match request["code"]:
            case "READ":
                self.logger.debug(f"READ request from {request['from_other']}")
                return protocol.Protocol.READ, self.read(request)
            case "WRITE":
                self.logger.debug(f"WRITE request to {request['to']} : {request['payload']}")
                return protocol.Protocol.WRITE, []
            case "LOGIN":
                self.logger.debug(f"LOGIN request ")
                return protocol.Protocol.LOGIN, []
                pass
            case "LOGOUT":
                return protocol.Protocol.LOGOUT, []
                pass
            case "REGISTER":
                return protocol.Protocol.REGISTER, []
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

    def read(self, request):
        return fetch_chat(request["from_other"])

