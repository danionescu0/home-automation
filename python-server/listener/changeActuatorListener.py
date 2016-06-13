from blinker import signal

class changeActuatorListener:
    def __init__(self, brain):
        self.__brain = brain
        changeActuatorRequest = signal("change_actuator_request")
        changeActuatorRequest.connect(self.callback)

    def callback(self, changeActuatorRequest):
        self.__brain.changeActuator(changeActuatorRequest.getName(), changeActuatorRequest.getNewState())
