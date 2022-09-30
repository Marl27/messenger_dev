import enum


class Protocol(enum.Enum):
    LOGOUT = 0
    LOGIN = 1
    REGISTER = 2
    READ = 3
    WRITE = 4
    LIST = 5

    @staticmethod
    def build_request(request_type: 'Protocol', to: str = "", sender: str = "", payload: str = ""):
        """
        Static method to
        :param request_type: header for function code (see protocol class)
        :param to: username
        :param sender: username
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
                packet = {"code": "READ", "sender": sender}
            case Protocol.WRITE:
                packet = {"code": "WRITE", "to": to, "payload": payload}
        return packet
