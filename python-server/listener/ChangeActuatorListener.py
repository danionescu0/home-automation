from blinker import signal
from typeguard import typechecked

from communication.actuator.ActuatorCommands import ActuatorCommands
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent

class ChangeActuatorListener:
    @typechecked()
    def __init__(self, actuator_commands: ActuatorCommands):
        self.__actuator_commands = actuator_commands
        signal("change_actuator_request").connect(self.callback)

    @typechecked()
    def callback(self, change_actuator_request: ChangeActuatorRequestEvent) -> None:
        self.__actuator_commands.change_actuator(change_actuator_request.get_name(), change_actuator_request.get_new_state())
