from typeguard import typechecked

from communication.actuator.AsyncActuatorCommands import AsyncActuatorCommands
from .BaseStrategy import BaseStrategy
from repository.ActuatorsRepository import ActuatorsRepository
from model.Actuator import Actuator
from model.ActuatorProperties import ActuatorProperties


class GroupStrategy(BaseStrategy):
    @typechecked()
    def __init__(self, actuators_repo: ActuatorsRepository, job_controll: AsyncActuatorCommands, logger):
        self.__actuators_repo = actuators_repo
        self.__job_controll = job_controll
        self.__logger = logger

    @typechecked()
    def supports(self, id: str) -> bool:
        return self.__actuators_repo.get_actuator(id).device_type == Actuator.DeviceType.GROUP.value

    @typechecked()
    def set_state(self, id: str, state) -> bool:
        actuator = self.__actuators_repo.get_actuator(id)

        for id in actuator.properties.get(ActuatorProperties.GROUP_ACTUATORS):
            self.__job_controll.change_actuator(id, actuator.properties.get(ActuatorProperties.GROUP_FUTURE_STATE))

        return True