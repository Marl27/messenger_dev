import asyncio
import json
import sys
from server.protocol import Protocol
from employee import Employee

HOSTNAME = "127.0.0.1"
PORT = 8888


def register():
    first_name = input("First name: ")
    print("Middle name: (leave blank if none)")
    middle_name = input("Middle name: ")
    last_name = input("Last name: ")
    username = input("Username: ")
    password = input("Password: ")
    start_date = input("Start date: ")
    print("Leaving date: (leave blank if unknown)")
    leaving_date = input("Leaving date: ")

    return Employee(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        username=username,
        password=password,
        start_date=start_date,
        leaving_date=leaving_date,
    )


class Client:
    def __init__(self, hostname: str, port: int, id: str = "default_client"):
        self.hostname = hostname
        self.port = port
        self.name = id

    async def tcp_echo_client(self, message: str):
        """
        Skeleton of a client program - not needed any more
        Interestingly, asyncio open_connection defaults to IPv6
        :param message: String to send
        :return:lz
        """

        # will change this to be command line input
        # either in a run loop after starting client program or from command line
        print(f"self.hostname = {self.hostname}, self.port = {self.port}")
        reader, writer = await asyncio.open_connection(self.hostname, self.port)
        print(f"Send request: {message!r}")
        # request = json.dumps(message, encoding="utf-8") +
        writer.write(bytes(json.dumps(message), encoding="utf-8"))
        await writer.drain()

        data = await reader.read(-1)
        print(f"Received: {data.decode()!r}")

        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    async def tcp_session_client(self):
        reader, writer = await asyncio.open_connection(self.hostname, self.port)
        print(f"Connected to server on {self.hostname}:{self.port}")

        # Login
        __authenticated = False
        while not __authenticated:
            print(f"Login or register: ")

            valid_choice = False
            while not valid_choice:
                login_or_register = input("> ")

                match login_or_register:
                    case "register":
                        valid_choice = True
                        registration = register()
                        registration_message = Protocol.build_request(
                            Protocol.REGISTER, employee=registration
                        )
                        print(f"Registration request: {registration_message}")
                        await Protocol.write_message(
                            json.dumps(registration_message).encode("utf-8"), writer
                        )
                        server_response = await Protocol.read_message(reader)
                        server_response = json.loads(server_response.decode("utf-8"))
                        print(f"Server response: {server_response}")

                    case "login":
                        valid_choice = True

            print(f"Please enter login credentials")
            username = input("Username: ")
            # How to hide the text like it does when logging in on linux?
            password = input("Password: ")

            login_message = Protocol.build_request(
                Protocol.LOGIN, username=username, password=password
            )
            await Protocol.write_message(
                json.dumps(login_message).encode("utf-8"), writer
            )
            server_response = await Protocol.read_message(reader)
            server_response = json.loads(server_response.decode("utf-8"))
            print(f"Server response: {server_response}")
            if server_response["authenticated"]:
                __authenticated = True
            else:
                print("Incorrect username or password.")

        print(f"Commands: read, write, test, quit")
        logout = False
        while not logout:
            message = {}
            command = input("> ")
            if command == "read":
                uid = input("Enter your user id> ")
                receiver = input("Read from whom? > ")
                message = Protocol.build_request(
                    Protocol.READ, receiver=receiver, sender=uid
                )

            elif command == "write":
                sender = input("Write to whom? >")
                message = input("Enter message >")
                message = Protocol.build_request(
                    Protocol.WRITE, sender=sender, payload=message
                )

            elif command == "test":
                message = TEST_PACKET

            elif command == "help":
                print(helpstring)
                continue

            elif command == "quit":
                message = Protocol.build_request(Protocol.LOGOUT, username=username)
                logout = True

            await Protocol.write_message(json.dumps(message).encode("utf-8"), writer)
            server_response = await Protocol.read_message(reader)
            server_response = json.loads(server_response.decode("utf-8"))
            print(f"Server response: {server_response}")

        writer.close()
        await writer.wait_closed()


client = None

TEST_PACKET = {
    "code": "LOGIN",
    "direction": Protocol.REQUEST.value,
    "sender": "Cruthe93",
    "message": 0xDEADBEEF,
    "testval": [x for x in range(10000)],
}

helpstring = "Commands: read, write, test, help, quit"

message = ""
# Not enough arguments
# if len(sys.argv) != 4:
#     print("Usage: client_async.py host port function")
#     print("Functions: login, register, read, write")
#     exit(1)
#
# elif len(sys.argv) == 4:
#     client = Client(id="Prototype", hostname=sys.argv[1], port=int(sys.argv[2]))
#
# print("Functions: login, register, read, write")
# if sys.argv[3] == "read":
#     uid = input("Enter your user id> ")
#     fro = input("Read from whom? > ")
#     message = Protocol.build_request(Protocol.READ, receiver=fro, sender=uid)
#
# elif sys.argv[3] == "write":
#
#     sender = input("Write to whom? >")
#     message = input("Enter message >")
#     message = Protocol.build_request(Protocol.WRITE, sender=sender, payload=message)
#
# elif sys.argv[3] == "test":
#     message = TEST_PACKET
client = Client(HOSTNAME, PORT)
asyncio.run(client.tcp_session_client(), debug=False)

# num_clients = 10
# # Creates 'num_clients' number of client objects with a random id number
# clients = [Client(id=str(random.randint(0, 100))) for x in range(num_clients)]

# while True:
#     for client in clients:
#     time.sleep(5)
