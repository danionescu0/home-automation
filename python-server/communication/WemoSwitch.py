from logging import RootLogger

from ouimeaux.environment import Environment
from ouimeaux.environment import UnknownDevice

from communication.DeviceLifetimeCycles import DeviceLifetimeCycles


class WemoSwitch(DeviceLifetimeCycles):
    def __init__(self, root_logger: RootLogger) -> None:
        self.__root_logger = root_logger
        self.__env = None

    def connect(self) -> None:
        try:
            self.__env = Environment()
            self.__env.start()
            self.__env.discover(seconds=5)
        except Exception as e:
            message = 'Got error while init WemoSwitch: {0} '.format(str(e))
            self.__root_logger.error(message)
            raise Exception(message)

    def disconnect(self) -> None:
        pass

    def change_state(self, actuator_name: str, state: bool) -> bool:
        try:
            switch = self.__env.get_switch(actuator_name)
            if (state):
                switch.on()
            else:
                switch.off()
        except UnknownDevice:
            self.__root_logger.error('Wemo device with name; {0} not found'.format(actuator_name))
            return False

        return True