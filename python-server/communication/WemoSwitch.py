from logging import RootLogger

from ouimeaux.environment import Environment
from ouimeaux.environment import UnknownDevice


class WemoSwitch:
    def __init__(self, root_logger: RootLogger) -> None:
        self.__root_logger = root_logger
        self.__env = None

    def connect(self) -> None:
        try:
            __env = Environment()
            __env.start()
            __env.discover(seconds=5)
        except Exception as e:
            self.__root_logger.error("Got error while init WemoSwitch" + str(e))
            self.__env = None

    def change_state(self, actuator_name: str, state):
        try:
            switch = self.__env.get_switch(actuator_name)
            if (state):
                switch.on()
            else:
                switch.off()
        except UnknownDevice:
            return False

        return True