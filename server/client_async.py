import asyncio
import random
import time
import json
import sys
from protocol import Protocol

HOSTNAME = "127.0.0.1"
PORT = 8888


class Client:

    def __init__(self, hostname: str = HOSTNAME, port: int = PORT, id: str = "default_client"):
        self.hostname = hostname
        self.port = port
        self.name = id

    async def tcp_echo_client(self, message: str):
        """
        Skeleton of a client program
        Interestingly, asyncio open_connection defaults to IPv6
        :param message: String to send
        :return:lz
        """

        # will change this to be command line input
        # either in a run loop after starting client program or from command line
        print(f"self.hostname = {self.hostname}, self.port = {self.port}")
        reader, writer = await asyncio.open_connection(self.hostname, self.port)
        print(f"Send request: {message!r}")
        writer.write(bytes(json.dumps(message), encoding="utf-8"))
        await writer.drain()

        data = await reader.read(100)
        print(f"Received: {data.decode()!r}")

        print("Close the connection")
        writer.close()
        await writer.wait_closed()

client = None
function = ""
message = ""
# Not enough arguments
if len(sys.argv) != 4:
    print("Usage: client_async.py host port function")
    print("Functions: login, register, read, write")
    exit(1)

elif len(sys.argv) == 4:
    client = Client(id="Prototype", hostname=sys.argv[1], port=int(sys.argv[2]))

print("Functions: login, register, read, write")
if sys.argv[3] == "read":
    function = "read"
    message = Protocol.build_request(Protocol.READ, to="", fro="", payload="")
    message2 = Protocol.build_request(Protocol.WRITE, to="", fro="", payload="TEST MESSAGE 0XDEADBEEF")

asyncio.run(client.tcp_echo_client(message), debug=True)
asyncio.run(client.tcp_echo_client(message2), debug=True)

# num_clients = 10
# # Creates 'num_clients' number of client objects with a random id number
# clients = [Client(id=str(random.randint(0, 100))) for x in range(num_clients)]

# while True:
#     for client in clients:
#     time.sleep(5)
