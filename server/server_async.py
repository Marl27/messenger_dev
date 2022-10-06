import asyncio
import logging
import sys
import json
from database import read_chat, login_or_register

from server.protocol import Protocol
# from main import HOSTNAME, PORT

# Default parameters
# HOSTNAME = HOSTNAME  # Should bind on all interfaces
# PORT = PORT  # arbitrary high level port


class Server:

    def __init__(self, hostname: str, port: int, logging_level: str = logging.WARN):
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
        Coroutine which handles incoming client sessions in parallel

        :param reader: asyncio.StreamReader - wrapper for async reading to TCP sockets
        :param writer: asyncio.StreamWriter - wrapper for async writing to TCP sockets
        :return:
        """
        addr = writer.get_extra_info("peername")
        self.logger.info(f"Client {addr} connected.")
        self.connected_clients.append(addr)  # Add this client to list of currently connected clients

        # Login
        login_request = await Protocol.read_message(reader)
        login_data = json.loads(login_request.decode())

        # here db_response has type (bool, employee_id)
        # if the login is a failure employee_id will be None
        # We know this is a login request so ignore the first return val
        _, db_response = self.parse_request(login_data)
        if not db_response[0]:
            # i.e. if the database returns an unsuccessful authentication
            # set client object's employee id
            pass

        # Passing bd_response in list to keep types passed to build_response the same
        # This should be refactored to pass a common type later on otherwise bugs
        #   will creep in
        login_response = await Protocol.build_response(Protocol.LOGIN, [db_response])
        login_response = json.dumps(login_response).encode("utf-8")
        await Protocol.write_message(login_response, writer)

        # Post login main loop
        logout = False
        while not logout:
            # reinitialise variables

            data = None
            message = {}
            response = {}

            data = await Protocol.read_message(
                reader)  # to run coroutines you need to call them using the 'await' keyword
            message = json.loads(data.decode())  # Decoding message from bytestream to utf-8 encoded text to json (dict)

            request_type, db_response = self.parse_request(message)
            self.logger.debug(f"request type: {request_type}, db_response: {type(db_response)}")
            # Ensures the rows returned from database contain the correct types for each position
            db_response = Server.database_type_coerce(request_type, db_response)
            self.logger.debug(f"Received {message!r} from {addr!r}")

            response = await Protocol.build_response(request_type, db_response)
            self.logger.debug(f"Response message: {response}")

            if response["code"] == "LOGOUT":
                self.logger.info(f"Client {addr!r} disconnected.")
                self.connected_clients.remove(addr)
                self.logger.debug(f"Connected clients: {self.connected_clients!r}")
                logout = True

            response = json.dumps(response).encode("utf-8")
            await Protocol.write_message(response, writer)

        # This method closes the stream AND the underlying socket
        writer.close()
        await writer.wait_closed()

    def parse_request(self, request: dict):
        """
        Method which parses client requests.
        The requests will be in json format
        NOTE this will need to be expanded to handle multiple requests in the one json file

        :param request: json format of request
        :return (Protocol type Enum, [database response]): Returns a tuple with the function code and relevant data from database
        """
        match request["code"]:
            case "READ":
                self.logger.debug(f"READ request from {request['from_other']}")
                return Protocol.READ, Server.read_from_db(request)
            case "WRITE":
                self.logger.debug(f"WRITE request to {request['to']} : {request['payload']}")
                return Protocol.WRITE, []
            case "LOGIN":
                self.logger.debug(f"LOGIN request from username {request['username']}")
                return Protocol.LOGIN, Server.login_db(request)
            case "LOGOUT":
                return Protocol.LOGOUT, []
            case "REGISTER":
                return Protocol.REGISTER, []

    async def main(self):
        """
        Entry point for server code
        :return:
        """
        # asyncio makes it easy to start tcp servers using start_server
        # It's already both IPv4 and IPv6
        server = await asyncio.start_server(self.handle_client, self.hostname, self.port)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        self.logger.info(f"Serving on {addrs}")

        async with server:
            await server.serve_forever()

    @staticmethod
    def read_from_db(request):
        # add to fetch_chat later: , request["from_other"]
        return read_chat.fetch_chat(request["to"])

    @staticmethod
    def login_db(request):
        return login_or_register.login(request["username"], request["password_hash"])

    @staticmethod
    def database_type_coerce(type, db_tuples):
        if type == Protocol.READ:
            updated_tuples = []
            for row in db_tuples:
                new_tuple = (
                    int(row[0]),
                    int(row[1]),
                    bool(row[2]),
                    str(row[3]),
                    str(row[4]),
                    bool(row[5]),
                    # This last one should eventually be changed to datetime
                    str(row[6])
                )
                updated_tuples.append(new_tuple)
        return db_tuples
