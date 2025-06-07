
class BookingException(Exception):
    def __init__(self, status_code, message, message_code):
        self.status_code = status_code
        self.message = message
        self.message_code = message_code
        super().__init__(message)