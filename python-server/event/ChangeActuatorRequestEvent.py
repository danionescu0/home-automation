from blinker import signal

class ChangeActuatorRequestEvent:
    def send(self, name, newState):
        event = signal("change_actuator_request")
        self.__name = name
        self.__newState = newState
        event.send(self)

    def get_name(self):
        return self.__name

    def getNewState(self):
        return self.__newState