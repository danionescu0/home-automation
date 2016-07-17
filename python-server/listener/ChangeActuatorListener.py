from blinker import signal

class ChangeActuatorListener:
    def __init__(self, actuatorCommands):
        self.__actuatorCommands = actuatorCommands
        changeActuatorRequest = signal("change_actuator_request")
        changeActuatorRequest.connect(self.callback)

    def callback(self, changeActuatorRequest):
        self.__actuatorCommands.change_actuator(changeActuatorRequest.getName(), changeActuatorRequest.getNewState())
