from typeguard import typechecked
from blinker import signal


class ChangeActuatorRequestEvent:
    @typechecked()
    def send(self, name: str, new_state) -> None:
        event = signal("change_actuator_request")
        self.__name = name
        self.__new_state = new_state
        event.send(self)

    @typechecked()
    def get_name(self) -> str:
        return self.__name

    @typechecked()
    def get_new_state(self):
        return self.__new_state