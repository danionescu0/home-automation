from listener.BaseListener import BaseListener


class ListenerConfigurator:
    def __init__(self):
        self.__listeners = []

    def register_listener(self, listener: BaseListener):
        self.__listeners.append(listener)

    def initialise(self):
        [listener.connect() for listener in self.__listeners]