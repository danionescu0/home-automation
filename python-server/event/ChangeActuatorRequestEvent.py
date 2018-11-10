from typeguard import typechecked


class ChangeActuatorRequestEvent:
    NAME = "change_actuator_request"

    @typechecked()
    def __init__(self, name: str, new_state) -> None:
        self.__name = name
        self.__new_state = new_state

    @typechecked()
    def get_name(self) -> str:
        return self.__name

    def get_new_state(self):
        return self.__new_state