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
                      sender: str = "",
                      receiver: str = "",
                      username="",
                      password="",
                      employee=None,
                      messenger=None):


        """
        Static method to build a request packet.
        :param messenger:
        :param password:
        :param username:
        :param sender:
        :param request_type: header for function code (see protocol class)
        :param receiver: username
        :param employee: employee object with their personal data
        :return packet: json representation of packet
        """

        packet = {}  # Empty packet
        match request_type:
            case Protocol.LOGOUT:
                packet = {"code": "LOGOUT", "username": username}

            case Protocol.LOGIN:
                packet = {"code": "LOGIN", "username": username, "password": password}

            case Protocol.REGISTER:
                packet = {
                    "code": "REGISTER",
                    "username": employee.username,
                    "password": employee.password,
                    "first_name": employee.first_name,
                    "middle_name": employee.middle_name,
                    "last_name": employee.last_name,
                    "start_date": employee.start_date,
                    "leaving_date": employee.leaving_date,
                }

            case Protocol.READ:
                # 1 = charlie
                # 2 = himalya
                # 3 = Random

                packet = {
                    "code": "READ",
                    "direction": Protocol.REQUEST.value,
                    "receiver": receiver,
                    "sender": sender,
                }

            case Protocol.WRITE:
                packet = {"code": "WRITE",
                          "direction": Protocol.REQUEST.value,
                          "sender": messenger.sender,
                          "receiver": messenger.receiver,
                          "is_broadcast": messenger.is_broadcasted,
                          "group_name": messenger.group_name,
                          "message": messenger.message,
                          "starred": messenger.is_stared
                          }

        return packet

    @staticmethod
    async def build_response(response_type: "Protocol", db_response: [(str)]) -> dict:
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
                packet = {
                    "code": "LOGOUT",
                    "direction": Protocol.RESPONSE.value,
                    "message": "goodbye",
                }

            case Protocol.LOGIN:
                packet = {
                    "code": "LOGIN",
                    "direction": Protocol.RESPONSE.value,
                    "authenticated": db_response[0][0],
                    "user_id": db_response[0][1],
                }

            case Protocol.REGISTER:
                packet = {
                    "code": "REGISTER",
                    "direction": Protocol.RESPONSE.value,
                }

            case Protocol.READ:
                # 1 = charlie
                # 2 = himalya
                # 3 = Random

                packet = {
                    "code": "READ",
                    "direction": Protocol.RESPONSE.value,
                    "messages": {},
                }
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
                packet = {
                    "code": "WRITE",
                    "direction": Protocol.RESPONSE.value,
                }
        return packet

    @staticmethod
    async def write_message(octets, writer):
        """
        Helper coroutine which prepends writes length of outgoing message first.

        :param octets: str - The message to send
        :param writer: asyncio.StreamWriter - The stream writer object
        :return:
        """
        writer.write(f"{len(octets)}\n".encode("utf-8"))
        writer.write(octets.encode("utf-8"))
        # Need to use write with drain as it might be queued in a write buffer
        # if it cannot be sent immediately
        await writer.drain()

    @staticmethod
    async def read_message(reader):
        """
        Helper coroutine which first reads the length of the incoming message
        then reads the exact number of bytes.

        :param reader: asyncio.StreamReader - the reader object
        :return :
        """
        prefix = await reader.readline()
        msg_len = 0
        if prefix:
            msg_len = int(prefix)
        msg = await reader.readexactly(msg_len)
        return msg.decode("utf-8")

    @staticmethod
    def extract_messages(message_chain):
        """
        Takes in a single message chain of type list of tuples and builds the response dictionary
        :param message_chain: list of tuples, each represents a single message and its metadata
        :return d: dictionary
        """
        num_messages = len(message_chain)
        d = {}
        def_dict = defaultdict(int)
        for i in range(num_messages):
            def_dict[i] += 1
        def_dict.default_factory = None
        d = dict(def_dict)

        for k, v in enumerate(d):
            d[k] = {
                "sender": message_chain[k][0],
                "receiver": message_chain[k][1],
                "is_broadcast": message_chain[k][2],
                "group_name": message_chain[k][3],
                "message": message_chain[k][4],
                "starred": message_chain[k][5],
                "created_at": message_chain[k][6],
            }
        return d


"""
Header fields:

code:   READ
        WRITE
        LOGIN
        LOGOUT
        REGISTER
        
read packet:
    receiver
    
write packet:
    sender
    payload (utf-8 message)
    
    
Database returns list of tuples for read each containing:
int UserId "sender" (the logged in user doing the read) 
int UserId "receiver" (user who sent the message to the logged in user)
bool broadcast (is the message a broadcast) 
int? groupId
string message
bool starred (i.e. favourited message)
datetime datetime

"""
