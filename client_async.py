import asyncio

HOST = "127.0.0.1"
PORT = 8888


async def tcp_echo_client(message: str):
    """
    Skeleton of a client program
    Interestingly, asyncio open_connection defaults to IPv6
    :param message: String to send
    :return:
    """

    # will change this to be command line input
    # either in a run loop after starting client program or from command line
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print(f"Send: {message!r}")
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f"Received: {data.decode()!r}")


# print("Close the connection")
# writer.close()
# await writer.wait_closed()

# Not sure if this is the correct way to loop on asyncio but it works
while True:
    asyncio.run(tcp_echo_client(input(">")), debug=True)
