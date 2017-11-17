from logging import RootLogger

from typeguard import typechecked

from repository.ActuatorsRepository import ActuatorsRepository
from communication.actuator.ActuatorStrategies import ActuatorStrategies
from model.Actuator import Actuator


class ActuatorCommands:
    @typechecked()
    def __init__(self, actuator_strategies: ActuatorStrategies, actuators_repo: ActuatorsRepository,
                 root_logger: RootLogger):
        self.__actuator_strategies = actuator_strategies
        self.__actuators_repo = actuators_repo
        self.__root_logger = root_logger
        self.__actuators = None

    @typechecked()
    def change_actuator(self, actuator_name: str, state):
        self.__actuators = self.__actuators_repo.get_actuators()
        self.__actuators_repo.set_actuator(actuator_name, state)
        #todo remove this return hack
        if self.__actuators[actuator_name].device_type == Actuator.DeviceType.ACTION.value:
            return

        strategy = self.__get_strategy(actuator_name)
        success = strategy.set_state(actuator_name, state)
        if not success and self.__actuators[actuator_name].type == Actuator.ActuatorType.SWITCH.value:
            self.__actuators_repo.set_actuator(actuator_name, not state)

        return success

    def __get_strategy(self, actuator_name):
        strategies = self.__actuator_strategies.get_strategies()
        try:
            return [strategy for strategy in strategies if strategy.supports(actuator_name)][0]
        except IndexError:
            raise NotImplementedError('Actuator {0} does not have a strategy associated. Check "device_type"'.format(actuator_name))