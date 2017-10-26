from logging import RootLogger


class ZWaveDevice:
    def __init__(self, root_logger: RootLogger) -> None:
        self.__root_logger = root_logger
        self.__env = None

    def connect(self) -> None:
        pass

    def change_state(self, actuator_name: str, state):
        pass