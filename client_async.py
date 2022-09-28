import asyncio

HOST

async def tcp_echo_client(message):
        """
        Skeleton of a client program
        Interestingly, asyncio open_connection defaults to IPv6
        :param message: String to send
        :return:
        """
        reader, writer = await asyncio.open_connection("localhost", 8888)
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
    asyncio.run(tcp_echo_client(input(">")))
