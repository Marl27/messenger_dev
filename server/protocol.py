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
                      username = "",
                      password = "",
                      payload: str = "",
                      employee=None):

        """
        Static method to build a request packet.
        :param request_type: header for function code (see protocol class)
        :param to: username
        :param from_other: username
        :param payload: string message
        :param employee: employee object with their personal data
        :return packet: json representation of packet
        """

        packet = {}  # Empty packet
        match request_type:
            case Protocol.LOGOUT:
                packet = {"code": "LOGOUT",
                          "username": username}

            case Protocol.LOGIN:
                packet = {"code": "LOGIN",
                          "username": username,
                          "password": password}

            case Protocol.REGISTER:
                packet = {"code": "REGISTER",
                          "username": employee.username,
                          "password": employee.password,
                          "first_name": employee.first_name,
                          "middle_name": employee.middle_name,
                          "last_name": employee.last_name,
                          "start_date": employee.start_date,
                          "leaving_date": employee.leaving_date}

            case Protocol.READ:
                # 1 = charlie
                # 2 = himalya
                # 3 = Random
                packet = {"code": "READ",
                          "direction": Protocol.REQUEST.value,
                          "from_other": from_other,
                          "to": to}

            case Protocol.WRITE:
                packet = {"code": "WRITE",
                          "direction": Protocol.REQUEST.value,
                          "to": to,
                          "payload": payload}
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
                          "direction": Protocol.RESPONSE.value,
                          "authenticated": db_response[0][0],
                          "user_id": db_response[0][1]}

            case Protocol.REGISTER:
                packet = {"code": "REGISTER",
                          "direction": Protocol.RESPONSE.value,
                          }

            case Protocol.READ:
                # 1 = charlie
                # 2 = himalya
                # 3 = Random

                packet = {"code": "READ",
                          "direction": Protocol.RESPONSE.value,
                          "messages": {}}
                # loop here

                if any(isinstance(el, list) for el in db_response):
                    # We know it's a list of lists
                    dlist = []
                    for chain in db_response:
                        for tuple in chain:
                            dlist.append(tuple)

                    packet["messages"] |= Protocol.extract_messages(dlist)
                else:
                    packet["messages"] |= Protocol.extract_messages(db_response)

            case Protocol.WRITE:
                packet = {"code": "WRITE",
                          "direction": Protocol.REQUEST.value, }
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

    # Takes in a single message chain of type list of tuples and builds the response dictionary
    @staticmethod
    def extract_messages(message_chain):
        num_messages = len(message_chain)
        d = {}
        def_dict = defaultdict(int)
        for i in range(num_messages):
            def_dict[i] += 1
        def_dict.default_factory = None
        d = dict(def_dict)

        for k, v in enumerate(d):
            d[k] = {"to": message_chain[k][0],
                    "from_other": message_chain[k][1],
                    "is_broadcast": message_chain[k][2],
                    "group_name": message_chain[k][3],
                    "message": message_chain[k][4],
                    "starred": message_chain[k][5],
                    "created_at": message_chain[k][6]}
        return d

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
