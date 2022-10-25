class Client:

    def __init__(self, host, port, username="", uid=-1):
        self.host = host
        self.port = port
        self.username = username
        self.uid = uid

    def __repr__(self):
        return f"{self.username} - {self.host}:{self.port}"