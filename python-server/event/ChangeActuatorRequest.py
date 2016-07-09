from blinker import signal

class ChangeActuatorRequest:
    def send(self, name, newState):
        event = signal("change_actuator_request")
        self.__name = name
        self.__newState = newState
        event.send(self)

    def getName(self):
        return self.__name

    def getNewState(self):
        return self.__newState