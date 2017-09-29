from typeguard import typechecked

from repository.ActuatorsRepository import ActuatorsRepository
from communication.actuator.ActuatorStrategiesBuilder import ActuatorStrategiesBuilder
from communication.encriptors.EncriptorsBuilder import EncriptorsBuilder


class ActuatorCommands:
    @typechecked()
    def __init__(self, actuator_strategy_builder: ActuatorStrategiesBuilder,
                 encriptors_builder: EncriptorsBuilder, actuators_repo: ActuatorsRepository, actuators_config: dict):
        self.__actuator_strategy_builder = actuator_strategy_builder
        self.__encriptors_builder = encriptors_builder
        self.__actuators_repo = actuators_repo
        self.__actuators_config = actuators_config

    @typechecked()
    def change_actuator(self, actuator_name: str, state: bool):
        self.__actuators_repo.set_actuator(actuator_name, state)
        if not self.__actuators_config[actuator_name]['strategy']:
            return

        strategy = self.__get_strategy(actuator_name)
        strategy = self.__configure_encription(strategy, actuator_name)
        success = strategy.toggle(actuator_name, state)
        if not success and self.__actuators_config[actuator_name]['type'] == 'bi':
            self.__actuators_repo.set_actuator(actuator_name, not state)

        return success

    def __get_strategy(self, actuator_name):
        strategies = self.__actuator_strategy_builder.build().get_strategies()
        try:
            return [strategy for strategy in strategies if strategy.supports(actuator_name)][0]
        except IndexError:
            raise NotImplementedError('Actuator {0} does not have a strategy associated'.format(actuator_name))

    def __configure_encription(self, strategy, actuator_name):
        if 'encription' in self.__actuators_config[actuator_name]:
            encription_strategy_type = self.__actuators_config[actuator_name]['encription']
        else:
            encription_strategy_type = 'plain'

        try:
            encription_strategies = self.__encriptors_builder.build().get_encriptors()

            return [strategy.set_encription(encription_strategy) for encription_strategy in encription_strategies
                    if encription_strategy.get_name() == encription_strategy_type][0]
        except IndexError:
            raise NotImplementedError('Actuator {0} does not have a strategy associated'.format(actuator_name))