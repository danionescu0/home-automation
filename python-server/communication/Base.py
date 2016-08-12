import abc

class Base:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.__endpoint = None
        self.__callback = None
        self.__logger = None

    @abc.abstractmethod
    def send(self, which, value):
        pass

    @abc.abstractmethod
    def listen(self, complete_message_callback, receive_message_callback):
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    def set_receive_message_callback(self, callback):
        self.__callback = callback

    def get_receive_message_callback(self):
        return self.__callback

    def set_logger(self, logger):
        self.__logger = logger

    def get_logger(self):
        return self.__logger