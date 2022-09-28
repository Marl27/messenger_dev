import asyncio

HOSTNAME = "localhost"  # ip: 127.0.0.1
PORT = 8888  # arbitrary high level port


class Server:

    def __init__(self):
        self.connected_clients = []  # List for now, might need to change data structure
        self.database = None  # Placeholder for database
        self.hostname = HOSTNAME
        self.port = PORT

        # Async def makes the function a 'coroutine'

    # basically a function that can be run using concurrency
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Coroutine which handles incoming client connections parallel
        :param reader: asyncio.StreamReader - wrapper for async reading to TCP sockets
        :param writer: asyncio.StreamWriter - wrapper for async writing to TCP sockets
        :return:
        """
        data = await reader.read(100)  # to run coroutines you need to call them using the 'await' keyword
        message = data.decode()  # Decoding message from bytestream to utf-8 encoded text
        addr = writer.get_extra_info("peername")
        self.connected_clients.append(addr) # Add this client to list of currently connected clients

        # TODO: change to use python logging module rather than print statements
        print(f"Received {message!r} from {addr!r}")
        print(f"Send: {message!r}")

        # Need to use write with drain as it might be queued in a write buffer
        # if it cannot be sent immediately
        writer.write(data)
        await writer.drain()

        # print("Close the connection")
        writer.close()

    # Returns a callback
    async def parse_command(self, input: str):
        """
        Coroutine which parses client commands
        :param input:
        :return: action (future)
        """
        pass

    async def main(self):
        # asyncio makes it easy to start tcp servers using start_server
        # It's already both IPv4 and IPv6
        server = await asyncio.start_server(self.handle_client, self.hostname, self.port)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {addrs}")

        async with server:
            await server.serve_forever()


# Remove debug=True when finished
server = Server()
asyncio.run(server.main(), debug=True)
