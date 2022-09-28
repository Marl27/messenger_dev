import asyncio
import random
import time

HOSTNAME = "127.0.0.1"
PORT = 8888


class Client:

    def __init__(self, hostname: str = HOSTNAME, port: int = PORT, name:str = "default_client"):
        self.hostname = hostname
        self.port = port
        self.name = name

    async def tcp_echo_client(self, message: str):
        """
        Skeleton of a client program
        Interestingly, asyncio open_connection defaults to IPv6
        :param message: String to send
        :return:
        """

        # will change this to be command line input
        # either in a run loop after starting client program or from command line
        reader, writer = await asyncio.open_connection(self.hostname, self.port)
        print(f"Send: {message!r}")
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        print(f"Received: {data.decode()!r}")

        print("Close the connection")
        writer.close()
        await writer.wait_closed()


num_clients = 10
clients = [Client(name=str(random.randint(0, 100))) for x in range(num_clients)]

while True:
    for client in clients:
        asyncio.run(client.tcp_echo_client(client.name), debug=True)
    time.sleep(5)
