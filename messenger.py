from database.read_chat import fetch_chat
from database.write_chat import write_chat


class Messenger:
    def __init__(self, sender, receiver, message="", is_broadcasted=False, group_name=None, is_stared=False):

        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.is_broadcasted = is_broadcasted
        self.group_name = group_name
        self.is_stared = is_stared

    def write_chat_to_messenger(self):
        if self.message != "":
            result = write_chat(self.sender, self.receiver, self.message, self.is_broadcasted, self.group_name,
                                self.is_stared)
            if result:
                return True

    def read_chat_from_messenger(self):
        return fetch_chat(self.sender, self.receiver)

