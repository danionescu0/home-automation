from pydispatch import dispatcher
from typeguard import typechecked

from communication.actuator.ActuatorCommands import ActuatorCommands
from event.ChangeActuatorRequestEvent import ChangeActuatorRequestEvent
from listener.BaseListener import BaseListener


class ChangeActuatorListener(BaseListener):
    @typechecked()
    def __init__(self, actuator_commands: ActuatorCommands):
        self.__actuator_commands = actuator_commands

    def connect(self):
        dispatcher.connect(self.listen, signal=ChangeActuatorRequestEvent.NAME, sender=dispatcher.Any)

    def listen(self, event: ChangeActuatorRequestEvent) -> None:
        self.__actuator_commands.change_actuator(
            event.get_name(), event.get_new_state()
        )