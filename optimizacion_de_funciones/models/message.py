from models.message_type import MessageType

class Message:

    def __init__(self, text: str, type: MessageType):
        self.text = text
        self.type = type

    def is_error(self):
        return self.type == MessageType.ERROR

    def is_warning(self):
        return self.type == MessageType.WARNING

    def is_info(self):
        return self.type == MessageType.INFO