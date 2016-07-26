from blinker import signal

class ChangeActuatorListener:
    def __init__(self, actuator_commands):
        self.__actuator_commands = actuator_commands
        change_actuator_request = signal("change_actuator_request")
        change_actuator_request.connect(self.callback)

    def callback(self, change_actuator_request):
        self.__actuator_commands.change_actuator(change_actuator_request.get_name(), change_actuator_request.getNewState())
