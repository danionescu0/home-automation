class Base:
    def __init__(self):
        self.__endpoint = None
        self.__callback = None
        self.__logger = None

    def set_endpoint(self, endpoint):
        self.__endpoint = endpoint

    def get_endpoint(self):
        return self.__endpoint

    def set_receive_message_callback(self, callback):
        self.__callback = callback

    def get_receive_message_callback(self):
        return self.__callback

    def set_logger(self, logger):
        self.__logger = logger

    def get_logger(self):
        return self.__logger