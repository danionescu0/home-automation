from typeguard import typechecked

from communication.actuator.AsyncActuatorCommands import AsyncActuatorCommands
from communication.actuator.strategies.BaseStrategy import BaseStrategy
from model.Actuator import Actuator
from model.ActuatorProperties import ActuatorProperties


class GroupStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, job_controll: AsyncActuatorCommands, logger):
        self.__job_controll = job_controll
        self.__logger = logger

    @typechecked()
    def supports(self, actuator: Actuator) -> bool:
        return actuator.device_type == Actuator.DeviceType.GROUP.value

    @typechecked()
    def set_state(self, actuator: Actuator, state) -> bool:
        for id in actuator.properties.get(ActuatorProperties.GROUP_ACTUATORS):
            self.__job_controll.change_actuator(id, actuator.properties.get(ActuatorProperties.GROUP_FUTURE_STATE))

        return True