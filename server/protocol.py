import enum


class Protocol(enum.Enum):
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
    def build_request(request_type: 'Protocol', to: str = "", from_other: str = "", payload: str = ""):
        """
        Static method to
        :param request_type: header for function code (see protocol class)
        :param to: username
        :param from_other: username
        :param payload: string message
        :return packet: json representation of packet
        """
        packet = {}  # Empty packet
        match request_type:
            case Protocol.LOGOUT:
                pass
            case Protocol.LOGIN:
                pass
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
    def build_response(response_type: 'Protocol', db_response: [(str)]):
        """
        TODO: Change to handle multiple database row responses
        :param response_type:
        :param db_response:
        :return:
        """
        packet = {}  # Empty packet
        match response_type:
            case Protocol.LOGOUT:
                pass
            case Protocol.LOGIN:
                pass
            case Protocol.REGISTER:
                pass
            case Protocol.READ:
                # 1 = charlie
                # 2 = himalya
                # 3 = Random
                packet = {"code": "READ",
                          "direction": Protocol.RESPONSE.value,
                          "to": db_response[0][0],
                          "from_other": db_response[0][1],
                          "is_broadcast": db_response[0][2],
                          "group_name": db_response[0][3],
                          "message": db_response[0][4],
                          "starred": db_response[0][5],
                          "created_at": db_response[0][6]}
            case Protocol.WRITE:
                packet = {"code": "WRITE", "direction": Protocol.REQUEST.value, }
        return packet


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
