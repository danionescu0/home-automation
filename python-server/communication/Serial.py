from communication.Base import Base

class Serial(Base):

    def __init__(self, endpoint):
        self.__endpoint = endpoint

    def connect(self):
        pass

    def disconnect(self):
        pass

    def send(self, which, value):
        print which, value
        pass

    def listen(self, complete_message_callback, receive_message_callback):
        pass


    def __get_endpoint(self):
        return self.__endpoint