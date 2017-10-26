from typing import List

from typeguard import typechecked

from communication.SerialCommunicatorRegistry import SerialCommunicatorRegistry
from communication.actuator.AsyncActuatorCommands import AsyncActuatorCommands
from communication.actuator.BaseStrategy import BaseStrategy
from communication.actuator.GroupStrategy import GroupStrategy
from communication.actuator.SerialSendStrategy import SerialSendStrategy
from communication.actuator.WemoSwitchStrategy import WemoSwitchStrategy
from communication.WemoSwitch import WemoSwitch
from repository.ActuatorsRepository import ActuatorsRepository


class ActuatorStrategiesBuilder():
    @typechecked()
    def __init__(self, communicator_registry: SerialCommunicatorRegistry, actuators_repo: ActuatorsRepository,
                 actuators_config: dict, async_actuator_commands: AsyncActuatorCommands, wemo_switch: WemoSwitch):
        self.__communicator_registry = communicator_registry
        self.__actuators_repo = actuators_repo
        self.__actuators_config = actuators_config
        self.__async_actuator_commands = async_actuator_commands
        self.__wemo_switch = wemo_switch
        self.__strategies = None

    def build(self):
        if None != self.__strategies:
            return self
        self.__strategies = []
        self.__strategies.append(
            SerialSendStrategy(self.__communicator_registry, self.__actuators_config, self.__actuators_repo))
        self.__strategies.append(WemoSwitchStrategy(self.__actuators_config, self.__wemo_switch))
        self.__strategies.append(GroupStrategy(self.__actuators_config, self.__async_actuator_commands))

        return self

    def get_strategies(self) -> List[BaseStrategy]:
        return self.__strategies