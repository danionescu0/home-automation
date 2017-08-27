from typing import List
from typeguard import typechecked

from communication.actuator.SerialSendStrategy import SerialSendStrategy
from communication.actuator.BaseStrategy import BaseStrategy
from communication.actuator.WemoSwitchStrategy import WemoSwitchStrategy
from communication.actuator.GroupStrategy import GroupStrategy
from communication.CommunicatorRegistry import CommunicatorRegistry
from repository.Actuators import Actuators
from tools.AsyncJobs import AsyncJobs

class ActuatorStrategiesBuilder():
    @typechecked()
    def __init__(self, communicator_registry: CommunicatorRegistry, actuators_repo: Actuators,
                 actuators_config: dict, job_controll: AsyncJobs):
        self.__communicator_registry = communicator_registry
        self.__actuators_repo = actuators_repo
        self.__actuators_config = actuators_config
        self.__job_controll = job_controll
        self.__strategies = None

    def build(self):
        if None != self.__strategies:
            return self
        self.__strategies = []
        self.__strategies.append(
            SerialSendStrategy(self.__communicator_registry, self.__actuators_config, self.__actuators_repo))
        self.__strategies.append(WemoSwitchStrategy(self.__actuators_config, self.__communicator_registry))
        self.__strategies.append(GroupStrategy(self.__actuators_config, self.__job_controll))

        return self

    def get_strategies(self) -> List[BaseStrategy]:
        return self.__strategies