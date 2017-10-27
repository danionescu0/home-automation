from typeguard import typechecked

from repository.ActuatorsRepository import ActuatorsRepository
from communication.actuator.ActuatorStrategies import ActuatorStrategies
from communication.encriptors.EncriptorsBuilder import EncriptorsBuilder


class ActuatorCommands:
    @typechecked()
    def __init__(self, actuator_strategies: ActuatorStrategies,
                 encriptors_builder: EncriptorsBuilder, actuators_repo: ActuatorsRepository):
        self.__actuator_strategies = actuator_strategies
        self.__encriptors_builder = encriptors_builder
        self.__actuators_repo = actuators_repo
        self.__actuators = None

    @typechecked()
    def change_actuator(self, actuator_name: str, state):
        self.__actuators = self.__actuators_repo.get_actuators()
        self.__actuators_repo.set_actuator(actuator_name, state)
        if not self.__actuators[actuator_name].strategy:
            return

        strategy = self.__get_strategy(actuator_name)
        strategy = self.__configure_encription(strategy, actuator_name)
        success = strategy.toggle(actuator_name, state)
        if not success and self.__actuators[actuator_name].type == 'bi':
            self.__actuators_repo.set_actuator(actuator_name, not state)

        return success

    def __get_strategy(self, actuator_name):
        strategies = self.__actuator_strategies.get_strategies()
        try:
            return [strategy for strategy in strategies if strategy.supports(actuator_name)][0]
        except IndexError:
            raise NotImplementedError('Actuator {0} does not have a strategy associated'.format(actuator_name))

    def __configure_encription(self, strategy: str, actuator_name: str):
        if self.__actuators[actuator_name].encription:
            encription_strategy_type = self.__actuators[actuator_name].encription
        else:
            encription_strategy_type = 'plain'
        try:
            encription_strategies = self.__encriptors_builder.build().get_encriptors()

            return [strategy.set_encription(encription_strategy) for encription_strategy in encription_strategies
                    if encription_strategy.get_name() == encription_strategy_type][0]
        except IndexError:
            raise NotImplementedError('Actuator {0} does not have a strategy associated'.format(actuator_name))