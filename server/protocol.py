import enum


class Protocol(enum.Enum):
    # Function codes
    LOGOUT = 0
    LOGIN = 1
    REGISTER = 2
    READ = 3
    WRITE = 4
    LIST = 5

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
                packet = {"code": "READ", "from_other": from_other}
            case Protocol.WRITE:
                packet = {"code": "WRITE", "to": to, "payload": payload}
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
"""