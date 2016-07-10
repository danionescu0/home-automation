class Base:
    def __init__(self):
        self.__endpoint = None
        self.__callback = None

    def setEndpoint(self, endpoint):
        self.__endpoint = endpoint

    def getEndpoint(self):
        return self.__endpoint

    def setReceiveMessageCallback(self, callback):
        self.__callback = callback

    def getReceiveMessageCallback(self):
        return self.__callback