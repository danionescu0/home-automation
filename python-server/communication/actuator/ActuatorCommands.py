from communication.actuator.SendStrategy import SendStrategy
from communication.actuator.WemoSwitchStrategy import WemoSwitchStrategy

class ActuatorCommands:
    def __init__(self, communicator_registry, actuators_repo, actuators_config):
        self.__communicator_registry = communicator_registry
        self.__actuators_repo = actuators_repo
        self.__actuators_config = actuators_config

    def change_actuator(self, actuator_name, state):
        self.__actuators_repo.set_actuator(actuator_name, state)
        if not self.__actuators_config[actuator_name]['strategy']:
            return
        self.__get_strategy(actuator_name).toggle(actuator_name, state)

    def __get_strategy(self, actuator_name):
        for strategy in self.__get_actuator_strategies():
            if strategy.supports(actuator_name):
                return strategy

        raise NotImplementedError('Actuator {0} does not have a strategy associated'.format(actuator_name))

    def __get_actuator_strategies(self):
        strategies = []
        strategies.append(SendStrategy(self.__communicator_registry, self.__actuators_config, self.__actuators_repo))
        strategies.append(WemoSwitchStrategy(self.__actuators_config))

        return strategies
