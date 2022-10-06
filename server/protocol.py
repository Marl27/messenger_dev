import enum
from collections import defaultdict


class Protocol(enum.Enum):
    """
    This class defines our application-layer protocol for client-server communication
    """
    # Function codes
    LOGOUT = 0
    LOGIN = 1
    REGISTER = 2
    READ = 3
    WRITE = 4
    LIST = 5
    REQUEST = 99
    RESPONSE = 100

    @staticmethod
    def build_request(request_type: 'Protocol',
                      to: str = "",
                      from_other: str = "",
                      payload: str = "",
                      username: str = "",
                      password_hash: str = ""):

        """
        Static method to build a request packet.
        :param request_type: header for function code (see protocol class)
        :param to: username
        :param from_other: username
        :param payload: string message
        :return packet: json representation of packet
        """

        packet = {}  # Empty packet
        match request_type:
            case Protocol.LOGOUT:
                packet = {"code": "LOGOUT", "username": username}
            case Protocol.LOGIN:
                packet = {"code": "LOGIN", "username": username, "password_hash": password_hash}
            case Protocol.REGISTER:
                pass
            case Protocol.READ:
                # 1 = charlie
                # 2 = himalya
                # 3 = Random
                packet = {"code": "READ", "direction": Protocol.REQUEST.value, "from_other": from_other, "to": to}
            case Protocol.WRITE:
                packet = {"code": "WRITE", "direction": Protocol.REQUEST.value, "to": to, "payload": payload}
        return packet

    @staticmethod
    async def build_response(response_type: 'Protocol', db_response: [(str)]) -> dict:
        """
        Static method to build a response packet. Takes a response code and builds appropriate packet
        using the response from the database.

        :param response_type: Can be one of: Protocol.LOGIN, Protocol.LOGOUT, Protocol.REGISTER, Protocol.READ, Protocol.WRITE
        :param db_response: - single tuple from the database
        :return packet: dict - json representation of the packet
        """
        packet = {}  # Empty packet
        match response_type:
            case Protocol.LOGOUT:
                packet = {"code": "LOGOUT",
                          "direction": Protocol.RESPONSE.value,
                          "message": "goodbye"}

            case Protocol.LOGIN:
                packet = {"code": "LOGIN",
                          "authenticated":db_response[0][0],
                          "user_id":db_response[0][1]}
            case Protocol.REGISTER:
                pass
            case Protocol.READ:
                # 1 = charlie
                # 2 = himalya
                # 3 = Random

                packet = {"code": "READ",
                          "direction": 100,
                          "messages": {}}

                num_messages = len(db_response)
                def_dict = defaultdict(int)
                for i in range(num_messages):
                    def_dict[i] += 1
                # Freeze default dict making it readonly
                def_dict.default_factory = None
                d = dict(def_dict)

                for k, v in enumerate(d):
                    d[k] = {"to": db_response[k][0],
                            "from_other": db_response[k][1],
                            "is_broadcast": db_response[k][2],
                            "group_name": db_response[k][3],
                            "message": db_response[k][4],
                            "starred": db_response[k][5],
                            "created_at": db_response[k][6]}

                packet["messages"] |= d

            case Protocol.WRITE:
                packet = {"code": "WRITE", "direction": Protocol.REQUEST.value, }
        return packet

    @staticmethod
    async def write_message(octets, writer):
        """
        Helper coroutine which prepends writes length of outgoing message first.

        :param octets: str - The message to send
        :param writer: asyncio.StreamWriter - The stream writer object
        :return:
        """
        writer.write(b"%d\n" % len(octets))
        writer.write(octets)
        # Need to use write with drain as it might be queued in a write buffer
        # if it cannot be sent immediately
        await writer.drain()

    @staticmethod
    async def read_message(reader):
        """
        Helper coroutine which first reads the length of the incoming message
        then reads the exact number of bytes.

        :param reader: asyncio.StreamReader - the reader object
        :return future:
        """
        prefix = await reader.readline()
        msg_len = 0
        if prefix:
            msg_len = int(prefix)
        return await reader.readexactly(msg_len)


"""
Header fields:

code:   READ
        WRITE
        LOGIN
        LOGOUT
        REGISTER
        
read packet:
    from_other
    
write packet:
    to
    payload (utf-8 message)
    
    
Database returns list of tuples for read each containing:
int UserId "to" (the logged in user doing the read) 
int UserId "from_other" (user who sent the message to the logged in user)
bool broadcast (is the message a broadcast) 
int? groupId
string message
bool starred (i.e. favourited message)
datetime datetime

"""
