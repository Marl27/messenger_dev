import asyncio
import logging
import sys
import json
from employee import Employee
from messenger import Messenger
from server.internal_client import Client

from server.protocol import Protocol
from user import User


# from main import HOSTNAME, PORT

# Default parameters
# HOSTNAME = HOSTNAME  # Should bind on all interfaces
# PORT = PORT  # arbitrary high level port


class Server:
    """
    Class which contains the core logic for the server.

    Attributes
    ----------
    hostname : str
        The IP address which the server is running from.

    port : int
        The port number which the server is bound to.

    conn : sqlite3.Connection
        Field for containing the database connection.

    cursor: sqlite3.Cursor
        Field for containing the database cursor object.

    logger: logging.Logger
        The server logging object. Default logging level set to logging.WARN

    connected_clients
        A list containing the connected client objects. Each object represents a unique client connected to the server.
    """
    def __init__(self, hostname: str, port: int, conn, cursor, logging_level: str = logging.WARN):
        self.connected_clients = []  # List for now, might need to change data structure
        self.hostname = hostname
        self.port = port
        self.conn = conn
        self.cursor = cursor
        self.logger = logging.getLogger("Server_logger")
        self.logger.setLevel(logging_level)
        logging.basicConfig(stream=sys.stdout, level=logging_level)

    # Async def makes the function a 'coroutine'
    # basically a function that can be run using concurrency
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Coroutine which handles incoming client sessions. Contains the main logic for managing a client session until they disconnect

        :param reader: asyncio.StreamReader - wrapper for async reading to TCP sockets
        :param writer: asyncio.StreamWriter - wrapper for async writing to TCP sockets
        :return:
        """
        addr = writer.get_extra_info("peername")
        self.logger.info(f"Client {addr} connected.")
        client = Client(*addr)
        self.connected_clients.append(client)  # Add this client to list of currently connected clients

        # Private variable to keep in login loop unless successful
        __authenticated = False
        while not __authenticated:
            # Login or register
            # to run coroutines you need to call them using the 'await' keyword
            login_register_request = await Protocol.read_message(reader)
            login_registration_data = json.loads(login_register_request.decode())
            client.username = login_registration_data["username"]
            self.logger.debug(f"Received : {login_registration_data}")
            # here db_response has type (bool, employee_id)
            # if the login is a failure employee_id will be None
            request_type, db_response = self.parse_request(login_registration_data)

            if db_response[1]:
                self.logger.info(f"Authentication success from {client.username} on {client.host, client.port}")
                client.uid = db_response[1]

            # Passing bd_response in list to keep types passed to build_response the same
            # This should be refactored to pass a common type later on otherwise bugs
            #   will creep in
            login_registration_response = await Protocol.build_response(request_type, [db_response])
            login_registration_response = json.dumps(login_registration_response).encode("utf-8")
            await Protocol.write_message(login_registration_response, writer)

            if request_type == Protocol.LOGIN and db_response[0]:
                # i.e. if the database returns a successful authentication
                __authenticated = True
        self.logger.debug(f"Connected clients: {self.connected_clients!r}")

        # Post login main loop
        logout = False
        while not logout:
            # reinitialise variables

            data = None
            message = {}
            response = {}

            data = await Protocol.read_message(reader)
            message = json.loads(data.decode())  # Decoding message from bytestream to utf-8 encoded text to json (dict)

            request_type, db_response = self.parse_request(message)
            self.logger.debug(f"request type: {request_type}, db_response: {type(db_response)}")
            # Ensures the rows returned from database contain the correct types for each position
            # db_response = Server.database_type_coerce(request_type, db_response)
            self.logger.debug(f"Received {message!r} from {addr!r}")

            response = await Protocol.build_response(request_type, db_response)
            self.logger.debug(f"Response message: {response}")

            if response["code"] == "LOGOUT":
                self.logger.info(f"Client {addr!r} disconnected.")
                self.connected_clients.remove(client)
                self.logger.debug(f"Connected clients: {self.connected_clients!r}")
                logout = True

            response = json.dumps(response).encode("utf-8")
            await Protocol.write_message(response, writer)

        # This method closes the stream AND the underlying socket
        writer.close()
        await writer.wait_closed()

    def parse_request(self, request: dict):
        """
        Method to parse a client request packet based on code field in headers. Packets have a 'code' field which can take one of the following values:
        Protocol.READ, Protocol.WRITE, Protocol.LOGIN, Protocol.LOGOUT, Protocol.REGISTER, Protocol.ERROR

        :param request: json format of request
        :return: Returns a tuple with the function code and relevant data from database.
        """
        match request["code"]:
            case "READ":
                self.logger.debug(f"READ request from {request['receiver']}")
                return Protocol.READ, Server.read_from_db(Messenger(conn=self.conn,
                                                                    cursor=self.cursor,
                                                                    sender=request["sender"],
                                                                    receiver=request["receiver"]))

            case "WRITE":
                self.logger.debug(f"WRITE request from {request['sender']} to {request['receiver']}"
                                  f" : {request['message']}")
                return Protocol.WRITE, Server.write_to_db(Messenger(conn=self.conn,
                                                                    cursor=self.cursor,
                                                                    sender=request["sender"],
                                                                    receiver=request["receiver"],
                                                                    is_broadcasted=request["is_broadcast"],
                                                                    group_name=request["group_name"],
                                                                    message=request["message"],
                                                                    is_stared=request["starred"]))

            case "LOGIN":
                self.logger.debug(f"LOGIN request from username {request['username']}")
                return Protocol.LOGIN, Server.login_db(user=User(conn=self.conn,
                                                                 cursor=self.cursor,
                                                                 username=request["username"],
                                                                 password=request["password"]))

            case "LOGOUT":
                self.logger.debug(f"LOGOUT request from username {request['username']}")
                return Protocol.LOGOUT, []

            case "REGISTER":
                self.logger.debug(f"REGISTER request from username {request['username']}")
                return Protocol.REGISTER, Server.register_db(Employee(conn=self.conn,
                                                                      cursor=self.cursor,
                                                                      username=request["username"],
                                                                      password=request["password"],
                                                                      first_name=request["first_name"],
                                                                      middle_name=request["middle_name"],
                                                                      last_name=request["last_name"],
                                                                      start_date=request["start_date"],
                                                                      leaving_date=request["leaving_date"]))

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
    def read_from_db(messenger):
        """
        Wrapper for reading from messenger object
        :param messenger:
        :return:
        """
        return messenger.read_chat_from_messenger()

    @staticmethod
    def write_to_db(messenger):
        """
        Wrapper for writing to messenger object
        :param messenger:
        :return:
        """
        return messenger.write_chat_to_messenger()

    @staticmethod
    def login_db(user: User):
        """
        Wrapper for logging in using User object
        :param user:
        :return:
        """
        # user can be of type user or employee
        return user.login()

    @staticmethod
    def register_db(employee: Employee):
        """
        Wrapper for registering a new employee user's details using Employee object
        :param employee:
        :return:
        """
        return employee.register_employee()

    # # fix me for multiple reads
    # @staticmethod
    # def database_type_coerce(type, db_tuples):
    #     if type == Protocol.READ and db_tuples is not None:
    #         updated_tuples = []
    #         for row in db_tuples:
    #             new_tuple = (
    #                 int(row[0]),
    #                 row[1],
    #                 bool(row[2]),
    #                 str(row[3]),
    #                 str(row[4]),
    #                 bool(row[5]),
    #                 # This last one should eventually be changed to datetime
    #                 str(row[6])
    #             )
    #             updated_tuples.append(new_tuple)
    #     return db_tuples
