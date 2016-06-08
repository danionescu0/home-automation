from blinker import signal

class actuatorChangedRequest:
    def send(self, name, newState):
        actuatorChangedRequest = signal("actuator_changed_request")
        self.__name = name
        self.__newState = newState
        actuatorChangedRequest.send(self)

    def getName(self):
        return self.__name

    def getNewState(self):
        return self.__newState