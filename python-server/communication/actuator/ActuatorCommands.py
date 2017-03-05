from communication.actuator.SerialSendStrategy import SerialSendStrategy
from communication.actuator.WemoSwitchStrategy import WemoSwitchStrategy
from communication.actuator.GroupStrategy import GroupStrategy
from communication.encriptors.AesEncriptor import AesEncriptor
from communication.encriptors.PlainTextEncriptor import PlainTextEncriptor

class ActuatorCommands:
    def __init__(self, communicator_registry, actuators_repo, actuators_config, aes_key, job_controll):
        self.__communicator_registry = communicator_registry
        self.__actuators_repo = actuators_repo
        self.__actuators_config = actuators_config
        self.__aes_key = aes_key
        self.__job_controll = job_controll

    def change_actuator(self, actuator_name, state):
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
        for strategy in self.__get_actuator_strategies():
            if strategy.supports(actuator_name):
                return strategy

        raise NotImplementedError('Actuator {0} does not have a strategy associated'.format(actuator_name))

    def __configure_encription(self, strategy, actuator_name):
        if 'encription' in self.__actuators_config[actuator_name]:
            encription_strategy_type = self.__actuators_config[actuator_name]['encription']
        else:
            encription_strategy_type = 'plain'

        for encription_strategy in self.__get_encription_strategies():
            if encription_strategy.get_name() == encription_strategy_type:
                return strategy.set_encription(encription_strategy)

        raise NotImplementedError('Actuator {0} does not have a strategy associated'.format(actuator_name))

    def __get_actuator_strategies(self):
        strategies = []
        strategies.append(SerialSendStrategy(self.__communicator_registry, self.__actuators_config, self.__actuators_repo))
        strategies.append(WemoSwitchStrategy(self.__actuators_config, self.__communicator_registry))
        strategies.append(GroupStrategy(self.__actuators_config, self.__job_controll))

        return strategies

    def __get_encription_strategies(self):
        encription_strategies = []
        encription_strategies.append(PlainTextEncriptor())
        encription_strategies.append(AesEncriptor(self.__aes_key))

        return encription_strategies